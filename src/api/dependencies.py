from typing import Generator
from sqlalchemy.orm import Session
from src.database.database import get_db
from src.utils.logging.log_client import LogClient
from src.config.logging_config import LOG_CLIENT_CONFIG

def get_db_session() -> Generator[Session, None, None]:
    return get_db()

def get_log_client() -> LogClient:
    return LogClient(
        host=LOG_CLIENT_CONFIG['HOST'],
        port=LOG_CLIENT_CONFIG['PORT']
    )
