import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os
import zlib
import base64

# TODO: Write tests for everything in this module

def bytes_to_base64(bytes_array):
    encoded_bytes = base64.b64encode(bytes_array)
    return encoded_bytes.decode('utf-8')

def base64_to_bytes(base64_string):
    decoded_bytes = base64.b64decode(base64_string)
    return decoded_bytes

def encrypt_aes_gcm(plaintext, key):
    '''
    Plaintext is a byte array. Key is a bytes string.
    '''

    # Apply SHA-256 hashing to the key
    hashed_key = hashlib.sha256(key).digest()

    # Generate a random 96-bit nonce
    nonce = os.urandom(12)

    # Encrypt the plaintext and leave aad blank
    aesgcm = AESGCM(hashed_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, b'')

    assert(len(nonce) == 12)
    return nonce + ciphertext # concats even if nonce is zeros

def decrypt_aes_gcm(ciphertext, key):
    '''Key is bytes.'''
    hashed_key = hashlib.sha256(key).digest()
    aesgcm = AESGCM(hashed_key)
    plaintext = aesgcm.decrypt(ciphertext[:12], ciphertext[12:], b'')
    return plaintext

def encrypt_class(c, key):
    '''
    Takes a Python class, pickels it and encrypts it with authenticated encryption.

    key may be a string or whatever.
    '''

    pickled = pickle.dumps(c)
    compressed = zlib.compress(pickled)
    ciphertext = encrypt_aes_gcm(compressed, key) # throws if validation fails
    return bytes_to_base64(ciphertext)

def decrypt_class(ciphertext, key):
    '''
    The encrypted class MUST use authenticated encryption or there is a security problem with the unpickeling process.
    '''

    ct = base64_to_bytes(ciphertext)
    plaintext = decrypt_aes_gcm(ct, key)
    decompressed = zlib.decompress(plaintext)
    c = pickle.loads(decompressed)
    return c

def derive_key_for_user(user):
    '''
    Uses the global secret and user's hashed password to derive a secret for that user.

    TODO: I have to think about what to do if the user changes their password.
    '''

    global_secret = b'TODO'
    user_secret = b'TODO'

    return hashlib.sha256(global_secret + user_secret).digest()

class Session:
    user = None
    embedded_class = None

def create_session_from_class(c, user):
    '''
    Creates a session blob from the class.

    The session blob is ... (describe theory here)
    '''

    session = Session()
    session.user =  user
    session.embedded_class = c

    key = derive_key_for_user(session.user)

    return encrypt_class(session, key)

def unpack_session_to_class(session, expected_user):
    '''
    Throws if there's a problem.

    TODO: Make sure it throws if there's a problem.
    '''

    key = derive_key_for_user(expected_user)
    decrypted = decrypt_class(session, key)

    if decrypted.user != expected_user:
        raise Exception('The session user does not match the expected user.')

    return decrypted.embedded_class






class foo:
    joel = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaoesuntaoeusnhaoeusnhaoesnutheoasnuaonuhnuouhet'

#f = foo()
#c = create_session_from_class(f, 'joel@example.com')
#print(c)
#print(len(c))
#f2 = unpack_session_to_class(c, 'joel@example.com')
#print(f2.joel)
#print(len(f2.joel))

