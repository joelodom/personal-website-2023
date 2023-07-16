import encrypted_session
import json

class TestClass:
    zip = 'zip'
    zap = [ 'zap' ]
    bang = 1234

def test_encrypted_session():
    print('Testing encrypted_session...')

    # test bytes and base64

    b = b'Hollywood Park'
    encoded = encrypted_session.bytes_to_base64(b)
    print(f'Encoded bytes: {encoded}')
    decoded = encrypted_session.base64_to_bytes(encoded)
    assert(decoded == b)

    # test encryption and decryption

    plaintext = b'We were born without time,'
    aad = b'Nameless in the arms of a mother, a father and God.'
    key = b'When the world would wait for us, a thousand years in the crush'

    ciphertext = encrypted_session.encrypt_aes_gcm(plaintext, aad, key)

    print(f'Ciphertext: {ciphertext}')

    plaintext_ = encrypted_session.decrypt_aes_gcm(ciphertext, aad, key)

    assert(plaintext == plaintext_)

    # failure tests

    try:
        ciphertext = encrypted_session.encrypt_aes_gcm(ciphertext, b'aoeu', key)
        assert(False) # should throw
    except:
        pass

    try:
        ciphertext = encrypted_session.encrypt_aes_gcm(ciphertext, aad, b'wrong key')
        assert(False) # should throw
    except:
        pass

    # test encrypting and decrypting a class
    
    aad = b'I could tell you you were all I ever wanted, dear.'

    c = TestClass()

    encrypted = encrypted_session.encrypt_class(c, aad, key)
    print(f'Encrypted class: {encrypted}')

    decrypted = encrypted_session.decrypt_class(encrypted, aad, key)

    assert(decrypted.zip == c.zip)
    assert(decrypted.zap == c.zap)
    assert(decrypted.bang == c.bang)

    # test bad email for session header

    bad_aad = b"I could utter every word you hoped you\'d hear."
    
    try:
        encrypted_session.decrypt_class(encrypted, bad_aad, key)
        assert(False) # should have failed
    except:
        pass

    # test new_session_id
    session_id = encrypted_session.new_session_id()
    session_id2 = encrypted_session.new_session_id()
    print(f'Session ID: {session_id}')
    assert(len(session_id) > 30)
    assert(session_id != session_id2)

    # test make_session_header_dict
    PRINCIPAL = 'joel@example.com'
    SEQUENCE_NUM = 3141
    d = encrypted_session.make_session_header_dict(
            PRINCIPAL, session_id, SEQUENCE_NUM)
    print(f'Session Header: {d}')
    assert(d[encrypted_session.SESSION_HEADER_VERSION] == encrypted_session.VERSION)
    assert(d[encrypted_session.SESSION_HEADER_PRINCIPAL] == PRINCIPAL)
    assert(d[encrypted_session.SESSION_HEADER_SESSION_ID] == session_id)
    assert(d[encrypted_session.SESSION_HEADER_SEQUENCE_NUM] == SEQUENCE_NUM)

    # test new_session

    PRINCIPAL = 'joel@example.com'
    session = encrypted_session.new_session(PRINCIPAL)

    d = session.header # so I can cut and paste from above
    assert(d[encrypted_session.SESSION_HEADER_VERSION] == encrypted_session.VERSION)
    assert(d[encrypted_session.SESSION_HEADER_PRINCIPAL] == PRINCIPAL)
    assert(d[encrypted_session.SESSION_HEADER_SEQUENCE_NUM] == 0)

    assert(session.session_data is not None)

    # test pack_session

    TEST_VALUE = 'To be used later to test unpacking'
    session.session_data.test_value = TEST_VALUE

    (aad, packed) = encrypted_session.pack_session(session)

    print(f'AAD: {aad}')
    print(f'Packed session: {packed}')

    # test sanitize_session_header (could use some failure tests...)
    d = json.loads(aad.decode())
    encrypted_session.sanitize_session_header(d)

    # test unpack_session

    unpacked = encrypted_session.unpack_session(aad, packed)

    d = session.header # so I can cut and paste from above
    assert(d[encrypted_session.SESSION_HEADER_VERSION] == encrypted_session.VERSION)
    assert(d[encrypted_session.SESSION_HEADER_PRINCIPAL] == PRINCIPAL)
    assert(d[encrypted_session.SESSION_HEADER_SEQUENCE_NUM] == 1)

    assert(unpacked.session_data.test_value == TEST_VALUE)

def run_all_tests():
    test_encrypted_session()

try:
    run_all_tests()
    print()
    print("=== No exceptions. All tests passed. ===")
    print()
except Exception as ex:
    print()
    print("*** EXCEPTIONS. TESTS FAILED. ***")
    print()
    raise(ex)
