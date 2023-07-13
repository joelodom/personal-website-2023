import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
import os

class SessionData:
    foo = 'foooooooooooooooooooo'

    def __str__(self):
        return self.foo

session = SessionData()
pickled = pickle.dumps(session)
unpickled = pickle.loads(pickled)

print(unpickled)


def encrypt_aes_gcm(plaintext, key):
    '''
    Plaintext is a byte array. Key may be a string or bytes because
    it will be hashed first.
    '''

    # Apply SHA-256 hashing to the key
    hashed_key = hashlib.sha256(key.encode('utf-8')).digest()

    # Generate a random 96-bit nonce
    nonce = os.urandom(12)

    # Encrypt the plaintext and leave aad blank
    aesgcm = AESGCM(hashed_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, b'')

    return (nonce, ciphertext)

def decrypt_aes_gcm(nonce, ciphertext, key):
    hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
    aesgcm = AESGCM(hashed_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, b'')
    return plaintext



plaintext = b'Joel was here...'
nonce, ciphertext = encrypt_aes_gcm(plaintext, 'key')
print(ciphertext)
plaintext = decrypt_aes_gcm(nonce, ciphertext, 'key')
print(plaintext)

def auth_encrypt(byte_str, key):
    '''
    Encrypts with authentication.
    '''



