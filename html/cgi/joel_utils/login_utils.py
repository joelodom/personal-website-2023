import mysql.connector
from . import my_secrets
from . import validation
import secrets
import hashlib

def get_user(email):
    '''
    returns (email, salt, password) or None.
    '''

    dbpw = my_secrets.get_secret(my_secrets.DATABASE_PASSWORD)

    # Connect to the MySQL server
    cnx = mysql.connector.connect(
        host='localhost',
        user='ubuntu',
        password=dbpw,
        database='website'
    )

    # Create a cursor object to interact with the database
    cursor = cnx.cursor()

    # Define the SQL query to select the row for the given email
    select_user_query = """
        SELECT email, salt, password FROM users
        WHERE email = %(email)s
    """

    # Define the parameter values for the query
    params = {'email': email}

    # Execute the query to select the user
    cursor.execute(select_user_query, params)

    # Fetch the row for the user
    user_row = cursor.fetchone()

    # Close the cursor and the connection
    cursor.close()
    cnx.close()

    return user_row # returns (email, salt, password)

def check_user(email, password):
    '''
    Checks a login. Returns false if the login fails. May throw.
    '''
    
    # First validate the input
    try:
        validation.validate_email_address(email)
        validation.validate_string_length(password, 1024)
    except validation.ValidationException as ex:
        print(ex)
        return

    print(f'Password: {password}')
    (email, db_salt, db_password) = get_user(email) # TODO: Throw more gracefully if user doesn't exist
    salt_bytes = bytes.fromhex(db_salt)
    print(f'<p>DB Salt: **{db_salt}**</p>')
    print(f'<p>Encoded DB Salt: **{salt_bytes}**</p>')
    encoded = password.encode("utf-8")  # Convert the password to bytes
    salted = hashlib.pbkdf2_hmac("sha256", encoded, salt_bytes, iterations=310000)

    print(f'DB PW: <p>**{db_password}**</p>    Salted: <p>**{salted.hex()}**</p>')

    if salted.hex() == db_password:
        return True

    return False


def new_user(email, password):
    '''
    Creates a new user. This function will validate the input and make sure the user doesn't exist already.
    '''

    # First validate the input
    try:
        validation.validate_email_address(email)
        validation.validate_string_length(password, 1024)
    except validation.ValidationException as ex:
        print(ex)
        return

    # Make sure the user doesn't already exist
    row = get_user(email)
    if row is not None:
        raise Exception('User already exists.') # TODO: This reveals who uses my website, so...???

    # Salt and hash the password

    salt = secrets.token_bytes(32)
    encoded = password.encode("utf-8")  # Convert the password to bytes
    salted = hashlib.pbkdf2_hmac("sha256", encoded, salt, iterations=310000)

    # Add the user

    dbpw = my_secrets.get_secret(my_secrets.DATABASE_PASSWORD)

    # Connect to the MySQL server
    cnx = mysql.connector.connect(
        host='localhost',
        user='ubuntu',
        password=dbpw,
        database='website'
    )
    
    # Create a cursor object to interact with the database
    cursor = cnx.cursor()
    
    # Define the data for the new entry
    new_entry = {
        'email': email,
        'salt': salt.hex(),
        'password': salted.hex()
    }
    
    # Define the SQL query to insert the new entry
    add_entry_query = """
        INSERT INTO users (email, salt, password)
        VALUES (%(email)s, %(salt)s, %(password)s)
    """
    
    # Execute the query to insert the new entry
    cursor.execute(add_entry_query, new_entry)
    
    # Commit the changes to the database
    cnx.commit()
    
    # Close the cursor and the connection
    cursor.close()
    cnx.close()
