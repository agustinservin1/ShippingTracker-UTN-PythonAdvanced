import re

def validate_address(func):
    def wrapper(*args, **kwargs):
        sender_address = kwargs.get('sender_address')
        recipient_address = kwargs.get('recipient_address')

        if not re.match(r'^[\w\s,.#-]{5,50}$', sender_address or ''):
            return "Error: Invalid sender address."
        if not re.match(r'^[\w\s,.#-]{5,50}$', recipient_address or ''):
            return "Error: Invalid recipient address."

        return func(*args, **kwargs)
    return wrapper

