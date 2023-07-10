#!/usr/bin/env python3

import cgi

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

