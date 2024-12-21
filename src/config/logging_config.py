import os
from dotenv import load_dotenv

load_dotenv() 

LOG_SERVER_CONFIG = {
    'HOST': os.getenv('LOG_SERVER_HOST', 'localhost'),
    'PORT': int(os.getenv('LOG_SERVER_PORT', 9999)),
    'LOG_DIR': os.getenv('LOG_DIR', 'logs'),
    'LOG_FILE': os.getenv('LOG_FILE', 'shipping_logs.txt'),
    'MAX_CONNECTIONS': int(os.getenv('MAX_CONNECTIONS', 5)),
    'SOCKET_TIMEOUT': int(os.getenv('SOCKET_TIMEOUT', 60))
}

LOG_CLIENT_CONFIG = {
    'HOST': os.getenv('LOG_CLIENT_HOST', 'localhost'),
    'PORT': int(os.getenv('LOG_CLIENT_PORT', 9999)),
    'MAX_RETRIES': int(os.getenv('MAX_RETRIES', 3)),
    'RETRY_DELAY': int(os.getenv('RETRY_DELAY', 2))
}