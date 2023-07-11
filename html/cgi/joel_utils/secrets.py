DATABASE_PASSWORD = 'db-passwd' # secret_key in MySQL

def get_secret(key):
    if key == DATABASE_PASSWORD:
        # special case
        with open('/home/ubuntu/personal-website-2023/db_passwd', 'r') as f:
            return f.read().strip()

print(f'--{get_secret(DATABASE_PASSWORD)}--')
