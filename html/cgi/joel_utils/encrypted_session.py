import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import zlib
import base64
import os
import json
import validation
import my_memcached
import db_utils
import my_secrets

def bytes_to_base64(bytes_array):
    encoded_bytes = base64.b64encode(bytes_array)
    return encoded_bytes.decode('utf-8')

def base64_to_bytes(base64_string):
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes

def encrypt_aes_gcm(plaintext, aad, key):
    '''
    All inputs are bytes. Key may be any length as it will be hashed first,
    but this doesn't add entropy.
    '''

    assert(isinstance(plaintext, bytes))
    assert(isinstance(aad, bytes))
    assert(isinstance(key, bytes))

    # Apply SHA-256 hashing to the key
    hashed_key = hashlib.sha256(key).digest()

    # Generate a random 96-bit nonce
    nonce = os.urandom(12)
    assert(len(nonce) == 12)

    # Encrypt the plaintext and leave aad blank
    aesgcm = AESGCM(hashed_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)

    return nonce + ciphertext # concats bytes strings regardless of leading zeros

def decrypt_aes_gcm(ciphertext, aad, key):
    '''
    All inputs are bytes.
    '''
    
    assert(isinstance(ciphertext, bytes))
    assert(isinstance(aad, bytes))
    assert(isinstance(key, bytes))

    hashed_key = hashlib.sha256(key).digest()
    aesgcm = AESGCM(hashed_key)
    plaintext = aesgcm.decrypt(ciphertext[:12], ciphertext[12:], aad)
    return plaintext

VERSION = 1 # The version of these sessions

SESSION_HEADER_VERSION = 'version'
SESSION_HEADER_PRINCIPAL = 'principal'
SESSION_HEADER_SESSION_ID = 'session-id'
SESSION_HEADER_SEQUENCE_NUM = 'sequence-num'

def make_session_header_dict(principal, session_id, sequence_num):
    return {
        SESSION_HEADER_VERSION: VERSION,
        SESSION_HEADER_PRINCIPAL: principal,
        SESSION_HEADER_SESSION_ID: session_id,
        SESSION_HEADER_SEQUENCE_NUM: sequence_num
    }

def unpack_session_header(j):
    '''
    Takes json and outputs session data.
    '''

    data = json.loads(j)

    return (int(data[SESSION_HEADER_VERSION]),
            data[SESSION_HEADER_PRINCIPAL],
            data[SESSION_HEADER_SESSION_ID],
            data[SESSION_HEADER_SEQUENCE_NUM])

def encrypt_class(c, aad, key):
    '''
    Takes a Python class, pickels it and encrypts it with authenticated encryption.
    '''

    pickled = pickle.dumps(c)
    compressed = zlib.compress(pickled)
    ciphertext = encrypt_aes_gcm(compressed, aad, key)
    return ciphertext

def decrypt_class(ciphertext, aad, key):
    '''
    The encrypted class MUST use authenticated encryption or there is a security problem with the unpickeling process. AAD is the EXPECTED AAD.
    '''

    plaintext = decrypt_aes_gcm(ciphertext, aad, key) # throws if validation fails
    decompressed = zlib.decompress(plaintext)
    c = pickle.loads(decompressed)
    return c

def derive_key(session_id, principal, seq_num):
    global_secret = my_secrets.get_secret(my_secrets.GLOBAL_SECRET)
    print(f"Global secret: {global_secret}")
    global_secret = base64_to_bytes(global_secret)

    user_secret = b'TODO'

    session_id_bytes = base64_to_bytes(session_id)
    
    sequence_num = str(seq_num).encode("utf-8")

    return hashlib.sha256(global_secret + user_secret + session_id_bytes + sequence_num).digest()

def new_session_id():
    return bytes_to_base64(os.urandom(32))

#######
#
# Move to the top and trace through and document.
# Remember to write the module top down and the tests bottoms up.
#
######

class SessionData:
    pass # caller may attach anything to this class

class Session:
    # these two key components must be assigned before class is used
    header = None # a dict with version, session id, principal, sequence number
    session_data = None

def new_session(principal):
    session = Session()
    session_id = new_session_id()
    session.header = make_session_header_dict(principal, session_id, 0)
    session.session_data = SessionData()
    return session

def pack_session(session):
   
    # increment the sequence number and update the cache

    before = session.header[SESSION_HEADER_SEQUENCE_NUM]
    session.header[SESSION_HEADER_SEQUENCE_NUM] += 1
    assert(session.header[SESSION_HEADER_SEQUENCE_NUM] == before + 1)

    # TODO: update the cache / database here

    # pack the session into an encrypted blob

    aad = json.dumps(session.header).encode('utf-8')
    key = derive_key(session.header[SESSION_HEADER_SESSION_ID],
        session.header[SESSION_HEADER_PRINCIPAL],
        session.header[SESSION_HEADER_SEQUENCE_NUM])
    encrypted = encrypt_class(session.session_data, aad, key)

    return (aad, encrypted)

def sanitize_session_header(header):
    # Takes a session header and performs basic validation and sanitization

    assert(header[SESSION_HEADER_VERSION] == VERSION)
    validation.validate_email_address(header[SESSION_HEADER_PRINCIPAL])
    assert(isinstance(header[SESSION_HEADER_SEQUENCE_NUM], int))
    assert(len(base64_to_bytes(header[SESSION_HEADER_SESSION_ID])) == 32)

def get_session_from_db(session_id):
    '''Takes b64-encoded 128-bit session id and returns (principal, expected_seq_num)'''

    # first try memcached
    memcached_client = my_memcached.MemcachedClient()
    session_from_mc = memcached.get(session_id)
    if session_from_mc is not None:
        session_from_mc.split(' ')
    
    # now go to the database
    query = f"SELECT principal, expected_seq_num FROM user_sessions WHERE session_id = '{session_id}'"
    with db_utils.MySQLDatabase() as db:
        result = db.execute_query(query, True)
    principal = result[0]
    expected_seq_num = result[1]

    # cache in memcached
    memcached_client.set(session_id, f"{principal} {expected_seq_num}")

    return (principal, expected_seq_num)

def unpack_session(aad, encrypted):

    # The aad is the header as bytes. Start by loading it into
    # a dictionary and performing some initial sanity checks.
    # The header and the encrypted session are bound together
    # by AES-GCM.

    session = Session()
    session.header = json.loads(aad.decode())
    
    sanitize_session_header(session.header)

    (principal, expected_seq_num) = get_session_from_db(
        session.header[SESSION_HEADER_SESSION_ID])

    # TODO: Validate that principal matches principal in header and validate sequence number
    # though I think that the way the key is derived is a belt-and-suspenders way of validating.

    # Decrypt

    key = derive_key(session_id, principal, expected_seq_num)
    session.session_data = decrypt_class(encrypted, aad, key)

    return session
