import os
from jinja2 import Template

def render_jinja(template):
    '''
    Resolves file relative to the caller, renders it, and adds HTTP headers.
    '''

    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_dir, template)

    with open(template_path, 'r') as f:
      template_string = f.read()

    template = Template(template_string)
    return template.render(name='Joel')








#import requests
#
#def get_html(url):
#    """
#    Fetches the HTML content of a given URL.
#    """
#    response = requests.get(url)
#    return response.text
#
#def download_file(url, destination):
#    """
#    Downloads a file from the given URL and saves it to the specified destination.
#    """
#    response = requests.get(url)
#    with open(destination, 'wb') as file:
#        file.write(response.content)
#
#class UserAgent:
#    """
#    A class to generate and manage User-Agent headers for HTTP requests.
#    """
#    def __init__(self, platform='Windows', browser='Chrome'):
#        self.platform = platform
#        self.browser = browser
#
#    def generate_header(self):
#        return f'Mozilla/5.0 ({self.platform}) AppleWebKit/537.36 (KHTML, like Gecko) {self.browser}/90.0.4430.212 Safari/537.36'
#
#    def set_user_agent_header(self):
#        header = self.generate_header()
#        requests.headers.update({'User-Agent': header})
#
