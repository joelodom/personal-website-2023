import my_memcached
import db_utils
import os
import encrypted_session

DATABASE_PASSWORD_FILE = '/home/ubuntu/personal-website-2023/db_passwd'

DATABASE_PASSWORD = 'db-passwd'
GLOBAL_SECRET = 'global-secret'

def get_secret(key):
    if key == DATABASE_PASSWORD: # special case
        with open(DATABASE_PASSWORD_FILE, 'r') as f:
            return f.read().strip()

    memcached_client = my_memcached.MemcachedClient()
    secret = memcached_client.get(key)[0]

    if secret is None:
        secret = get_secret_from_database(key)[0]
        if secret is None:
            raise Exception(f"Could not fetch secret {key}")
        memcached_client.set(key, secret)

    return secret

def get_secret_from_database(key):
    query = f"SELECT secret_value FROM secrets WHERE secret_key = '{key}'"
    with db_utils.MySQLDatabase() as db:
        result = db.execute_query(query, True)
        return result[0]

def create_global_secret_in_database():
    query = f"SELECT secret_value FROM secrets WHERE secret_key = '{GLOBAL_SECRET}'"
    with db_utils.MySQLDatabase() as db:
        result = db.execute_query(query, True)
        assert(len(result) == 0) # makes sure it's not already in there
        secret = os.urandom(32)
        secret = encrypted_session.bytes_to_base64(secret)
        query = f"INSERT INTO secrets (secret_key, secret_value) VALUES ('{GLOBAL_SECRET}', '{secret}')"
        db.execute_query(query, False)
