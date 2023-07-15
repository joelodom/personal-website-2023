import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import zlib
import base64
import os
import json

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

HEADER_VERSION = 'version'
HEADER_PRINCIPAL = 'principal'

def make_session_header(email):
    '''
    Outputs JSON to be used as AAD for the session.
    '''

    data = {
        HEADER_VERSION: VERSION,
        HEADER_PRINCIPAL: email
    }

    return json.dumps(data)

def unpack_session_header(j):
    '''
    Takes json and outputs version and email.
    '''

    data = json.loads(j)

    return (int(data[HEADER_VERSION]), data[HEADER_PRINCIPAL])
    

def encrypt_class(c, aad, key):
    '''
    Takes a Python class, pickels it and encrypts it with authenticated encryption.
    '''

    pickled = pickle.dumps(c)
    compressed = zlib.compress(pickled)
    ciphertext = encrypt_aes_gcm(compressed, aad, key) # throws if validation fails
    return bytes_to_base64(ciphertext)

def decrypt_class(ciphertext, aad, key):
    '''
    The encrypted class MUST use authenticated encryption or there is a security problem with the unpickeling process. AAD is the EXPECTED AAD.
    '''

    ct = base64_to_bytes(ciphertext)
    plaintext = decrypt_aes_gcm(ct, aad, key)
    decompressed = zlib.decompress(plaintext)
    c = pickle.loads(decompressed)
    return c

def derive_key_for_user(user):
    '''
    Uses the global secret and user's hashed password to derive a secret for that user.
    '''

    global_secret = b'TODO'
    user_secret = b'TODO'

    return hashlib.sha256(global_secret + user_secret).digest()

def create_session_from_class(c, user):
    '''
    Creates a session blob from the class.
    '''

    key = derive_key_for_user(user)
    aad = make_session_header(user).encode('utf-8')
    return encrypt_class(c, aad, key)

def unpack_session_to_class(session, expected_user):
    '''
    Throws if there's a problem.

    TODO: Make sure it throws if there's a problem.
    '''

    key = derive_key_for_user(expected_user)
    expected_aad = make_session_header(expected_user).encode('utf-8')
    decrypted = decrypt_class(session, expected_aad, key)

    return decrypted
