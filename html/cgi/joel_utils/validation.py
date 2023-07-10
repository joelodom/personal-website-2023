import re
import email.utils

class ValidationException(Exception):
    pass

def validate_email_address(email_address):
    try:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            raise ValidationException()
        email.utils.parseaddr(email_address) # I think this raises, too.
    except:
        raise ValidationException('Invalid email address')

def validate_string_length(string, max_length):
    if len(string) > max_length:
        raise ValidationException('String too long')
