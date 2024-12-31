import socket
import json
import logging
from typing import Dict, Any
from datetime import datetime

class LogClient:
    def __init__(self, host: str = 'localhost', port: int = 5000):
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def connect(self) -> bool:
        """Establishes connection with the log server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.logger.info(f"Connected to log server at {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"Error connecting to the server: {e}")
            self.connected = False
            return False

    def send_log(self, service: str, message: str, level: str = "INFO", extra: Dict[str, Any] = None) -> bool:
        """Sends a log message to the server"""
        if not self.connected:
            if not self.connect():
                return False

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "message": message,
            "level": level,
            "extra": extra or {}
        }

        try:
            self.socket.send(json.dumps(log_entry).encode())
            return True
        except Exception as e:
            self.logger.error(f"Error sending log: {e}")
            self.connected = False
            return False

    def close(self):
        """Closes the connection with the server"""
        if self.socket:
            try:
                self.socket.close()
                self.connected = False
                self.logger.info("Connection closed")
            except Exception as e:
                self.logger.error(f"Error closing the connection: {e}")
