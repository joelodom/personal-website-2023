#!/usr/bin/env python3

import cgi
import hashlib
import secrets

# Create instance of FieldStorage
form = cgi.FieldStorage()

# Get the values from the form fields
email = form.getvalue('email')
password = form.getvalue('password')

# Set the content type to HTML
print("Content-type: text/html\n")

# Display the received email and password
print("<h2>Received Data:</h2>")
print("<p>Email: {}</p>".format(email))
print("<p>Password: {}</p>".format(password))


password = password.encode("utf-8")  # Convert the password to bytes
salt = secrets.token_bytes(16)

key = hashlib.pbkdf2_hmac("sha256", password, salt, iterations=310000)

# The derived key can be used for encryption, authentication, or other purposes
print(f"<p>Key: {key.hex()}</p>")

