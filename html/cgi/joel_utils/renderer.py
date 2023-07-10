import os
from jinja2 import Template
from . import system_utils

def render_jinja(template, **kwargs):
    '''
    Resolves file relative to the caller, renders it, and adds HTTP headers.
    '''

    caller_file = system_utils.get_caller_path()
    template_path = system_utils.get_absolute_path(caller_file, template)

    with open(template_path, 'r') as f:
      template_string = f.read()

    template = Template(template_string)
    return template.render(kwargs)
