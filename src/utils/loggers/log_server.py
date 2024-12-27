import socket
import threading
import json
import os
import signal
from datetime import datetime
from typing import Dict
import logging
from src.config.logging_config import LOG_SERVER_CONFIG

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LogServer:
    def __init__(self):

        self.host = LOG_SERVER_CONFIG['HOST']   
        self.port = LOG_SERVER_CONFIG['PORT']
        self.log_dir = LOG_SERVER_CONFIG['LOG_DIR']
        self.log_file = os.path.join(self.log_dir, LOG_SERVER_CONFIG['LOG_FILE'])
        self.max_connections = LOG_SERVER_CONFIG['MAX_CONNECTIONS']
        self.socket_timeout = LOG_SERVER_CONFIG['SOCKET_TIMEOUT']
        
        self.running = False
        self.server_socket = None
        self.clients: Dict[str, socket.socket] = {}
        
        os.makedirs(self.log_dir, exist_ok=True)
        
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):

        """Handles graceful server shutdown"""
        logging.info("Shutdown signal received. Closing server...")
        self.stop()

    def start(self):
        
        """Starts the log server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)  
            self.running = True
            logging.info(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client, addr = self.server_socket.accept()
                    client_id = f"{addr[0]}:{addr[1]}"
                    self.clients[client_id] = client
                    logging.info(f"New connection from {client_id}")

                        # Start thread to handle client
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client, client_id),
                        daemon=True
                    )
                    
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        logging.error(f"Error accepting connections: {e}")
                        
        except Exception as e:
            logging.error(f"Error starting server: {e}")

        finally:
            self.stop()

    def stop(self):

        """Stops the server and closes all connections"""
        if self.running:
            self.running = False 
            logging.info("Stopping server...") 

            # Close all client connections
            for client_id, client_socket in list(self.clients.items()):
                try: 
                    client_socket.close()
                    logging.info(f"Connection closed: {client_id}")
                except Exception as e: 
                    logging.error(f"Error closing client {client_id}: {e}")
                    self.clients.pop(client_id, None)

            # Close server socket 
            if self.server_socket:
                 try: self.server_socket.close()
                 except Exception as e:
                     logging.error(f"Error closing server socket: {e}") 
                     
            logging.info("Server stopped")

    def _handle_client(self, client_socket: socket.socket, client_id: str):
        
        """Handles a client's connection"""
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                self._process_log(data.decode(), client_id)
        except Exception as e:
            logging.error(f"Error with client {client_id}: {e}")
        finally:
            client_socket.close()
            self.clients.pop(client_id, None)
            logging.info(f"Client disconnected: {client_id}")

    def _process_log(self, data: str, client_id: str):
        """Processes a log entry received from a client"""
        try:
            log_entry = json.loads(data)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            formatted_log = (
                f"[{timestamp}] {client_id} | "
                f"Level: {log_entry.get('level', 'INFO')} | "
                f"Service: {log_entry.get('service', 'Unknown')} | "
                f"Message: {log_entry.get('message', 'No message')}"
            )
            
            if extra := log_entry.get('extra'):
                formatted_log += f" | Extra: {json.dumps(extra)}"

            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_log + '\n')
                
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON from {client_id}: {e}")
        
        except Exception as e:
            logging.error(f"Error processing log from {client_id}: {e}")

if __name__ == "__main__":

    server = LogServer()
    
    try:
        server.start()
    
    except KeyboardInterrupt:
        logging.info("Server stopped by user")  
    
    finally:
        server.stop()