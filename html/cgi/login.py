#!/usr/bin/env python3

import os
#import joels_web_utils





from jinja2 import Template

# Get the directory of the current Python script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the template file relative to the script directory
template_path = os.path.join(script_dir, '../templates/login.jinja2')

# Read the contents of the template file
with open(template_path, 'r') as f:
    template_string = f.read()

# Create a Jinja Template object using the template string
template = Template(template_string)

# Render the template with the provided context
rendered = template.render(name="John")

# Print the rendered output
print(rendered)

