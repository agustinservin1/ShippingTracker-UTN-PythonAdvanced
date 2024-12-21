from functools import wraps
from typing import Callable
import re
def validate_address(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0] if args else None
        sender_address = request.sender_address if request else None
        recipient_address = request.recipient_address if request else None
        
        if not re.match(r'^[\w\s,.#-]{5,50}$', sender_address or ''):
            raise ValueError("Error: Invalid sender address.")
        if not re.match(r'^[\w\s,.#-]{5,50}$', recipient_address or ''):
            raise ValueError("Error: Invalid recipient address.")
        return func(*args, **kwargs)
    return wrapper
