import my_memcached

DATABASE_PASSWORD_FILE = '/home/ubuntu/personal-website-2023/db_passwd'

DATABASE_PASSWORD = 'db-passwd'
GLOBAL_SECRET = 'global-secret'

def get_secret(key):
    if key == DATABASE_PASSWORD: # special case
        with open(DATABASE_PASSWORD_FILE, 'r') as f:
            return f.read().strip()

    memcached_client = my_memcached.MemcachedClient()
    secret = memcached_client.get(key)

    if secret is None:
        secret = get_secret_from_database(key)
        if secret is None:
            raise Exception(f"Could not fetch secret {key}")
        memcached_client.set(key, secret)

    return secret
