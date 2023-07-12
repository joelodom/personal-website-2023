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
    
    # Create the user
    # IMPORTANT: new_user must validate the input and make sure the user doesn't exist
    login_utils.new_user(email, password)
except Exception as ex:
    print(f'<p>Exception: {ex}</p>')
    exit(-1)


# Display the received email and password
print("<h2>Received Data:</h2>")
print("<p>Email: {}</p>".format(email))
print("<p>Password: {}</p>".format(password))

print('<p>New user created!</p>')
