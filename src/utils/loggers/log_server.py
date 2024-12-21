import socket
import threading
import json
import os
from datetime import datetime
from typing import Dict, Any
import logging
from src.config.logging_config import LOG_SERVER_CONFIG
# Configuración del log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LogServer:
    def __init__(self):
        self.host = LOG_SERVER_CONFIG['HOST']
        self.port = LOG_SERVER_CONFIG['PORT']
        self.log_file = os.path.join(LOG_SERVER_CONFIG['LOG_DIR'], LOG_SERVER_CONFIG['LOG_FILE'])
        self.running = False
        self.clients: Dict[str, socket.socket] = {}
        os.makedirs(LOG_SERVER_CONFIG['LOG_DIR'], exist_ok=True)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen(LOG_SERVER_CONFIG['MAX_CONNECTIONS'])
            self.running = True
            logging.info(f"Log server started on {self.host}:{self.port}")

            while self.running:
                try:
                    client, addr = server.accept()
                    client_id = f"{addr[0]}:{addr[1]}"
                    self.clients[client_id] = client
                    logging.info(f"New connection from {client_id}")
                    threading.Thread(target=self._handle_client, args=(client, client_id), daemon=True).start()
                except Exception as e:
                    logging.error(f"Server error: {e}")
                    self.running = False

    def _handle_client(self, client_socket: socket.socket, client_id: str):
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                self._process_logs(data.decode())
        except Exception as e:
            logging.error(f"Error handling client {client_id}: {e}")
        finally:
            client_socket.close()
            self.clients.pop(client_id, None)

    def _process_logs(self, data: str):
        try:
            for entry in data.strip().split('\n'):
                log_entry = json.loads(entry)
                self._write_log(log_entry)
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")

    def _write_log(self, log_entry: Dict[str, Any]):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted_log = (
            f"[{timestamp}] Level: {log_entry.get('level', 'INFO')} | "
            f"Service: {log_entry.get('service', 'Unknown')} | "
            f"Action: {log_entry.get('action', 'Unknown')} | "
            f"Message: {log_entry.get('message', 'No message')}"
        )
        if extra := log_entry.get('extra'):
            formatted_log += f" | Extra: {json.dumps(extra)}"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(formatted_log + '\n')

if __name__ == "__main__":
     server = LogServer()
     logging.info("Starting log server...")
     server.start()