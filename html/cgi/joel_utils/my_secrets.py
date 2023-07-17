import my_memcached

DATABASE_PASSWORD = 'db-passwd'
GLOBAL_SECRET = 'global-secret'

def get_secret(key):
    if key == DATABASE_PASSWORD:
        # special case
        with open('/home/ubuntu/personal-website-2023/db_passwd', 'r') as f:
            return f.read().strip()

    secret = get_secret_from_memcached(key)

    if secret is None:
        secret = get_secret_from_database(key)
        if secret is None:
            raise Exception(f"Could not fetch secret {key}")
        set_secret_in_memcached(key, value)

    return secret

def get_secret_from_memcached(key):
    raise NotImplemented()

def set_secret_in_memcached(key, value):
    raise NotImplemented()

def get_secret_from_database(key):
    raise NotImplemented()
