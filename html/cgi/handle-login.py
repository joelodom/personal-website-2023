#!/usr/bin/env python3

import cgi
from joel_utils import login_utils

# Set the content type to HTML
print("Content-type: text/html\n")

try:
    # Create instance of FieldStorage
    form = cgi.FieldStorage()
    
    # Get the values from the form fields
    email = form.getvalue('email')
    password = form.getvalue('password')
    
    # Check the credentials
    # IMPORTANT: check_user must validate the input and make sure the credentials are valid
    if not login_utils.check_user(email, password):
        raise Exception('Invalid login')
except Exception as ex:
    print(f'<p>Exception: {str(ex)}</p>')
    exit(-1)


# Display the received email and password
print("<h2>Received Data:</h2>")
print("<p>Email: {}</p>".format(email))
print("<p>Password: {}</p>".format(password))

print('<p>Login success!</p>')
