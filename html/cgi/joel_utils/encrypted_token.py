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
    Plaintext is a byte array. Key may be a string or bytes because
    it will be hashed to 256 bits (not that that adds any entropy).
    '''

    # Apply SHA-256 hashing to the key
    hashed_key = hashlib.sha256(key.encode('utf-8')).digest()

    # Generate a random 96-bit nonce
    nonce = os.urandom(12)

    # Encrypt the plaintext and leave aad blank
    aesgcm = AESGCM(hashed_key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, b'')

    assert(len(nonce) == 12)
    return nonce + ciphertext # concats even if nonce is zeros

def decrypt_aes_gcm(ciphertext, key):
    hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
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

#class foo:
#    joel = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaoesuntaoeusnhaoeusnhaoesnutheoasnuaonuhnuouhet'
#
#f = foo()
#c = encrypt_class(f, 'key')
#print(c)
#print(len(c))
#f2 = decrypt_class(c, 'key')
#print(f2.joel)
#print(len(f2.joel))

