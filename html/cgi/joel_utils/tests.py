import encrypted_session

class TestClass:
    zip = 'zip'
    zap = [ 'zap' ]
    bang = 1234

def test_encrypted_session():
    print('Testing encrypted_session...')

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

    print()

    # test packing and unpacking JSON header

    email = 'joel@example.com'
    j = encrypted_session.make_session_header(email)
    print(f'Session header: {j}')
    (v, e) = encrypted_session.unpack_session_header(j)
    assert(v == encrypted_session.VERSION)
    assert(e == email)

    # test encrypting and decrypting a class
    
    aad = j.encode('utf-8') # this is how I plan to actually use it, anyway

    c = TestClass()

    encrypted = encrypted_session.encrypt_class(c, aad, key)
    print(f'Encrypted class: {encrypted}')

    decrypted = encrypted_session.decrypt_class(encrypted, aad, key)

    assert(decrypted.zip == c.zip)
    assert(decrypted.zap == c.zap)
    assert(decrypted.bang == c.bang)

    # test bad email for session header

    bad_aad = encrypted_session.make_session_header('nope@example.com')
    
    try:
        encrypted_session.decrypt_class(encrypted, bad_aad, key)
        assert(False) # should have failed
    except:
        pass

    # test making a session from a class

    session = encrypted_session.create_session_from_class(c, email)
    print(f'Session: {session}')

    decrypted = encrypted_session.unpack_session_to_class(session, email)

    assert(decrypted.zip == c.zip)
    assert(decrypted.zap == c.zap)
    assert(decrypted.bang == c.bang)

    # test tampering with session

    TEST_INDEX = 6 # arbitrary
    replacement = 'a' if session[TEST_INDEX] != 'a' else 'b'
    session = session[:TEST_INDEX] + replacement + session[TEST_INDEX:]

    try:
        decrypted = encrypted_session.unpack_session_to_class(session, email)
        assert(False) # should have failed
    except:
        pass


def run_all_tests():
    test_encrypted_session()

run_all_tests()
