# logstash_handler.py

import logging
import socket
import json

class LogstashTCPHandler(logging.Handler):
    def __init__(self, host='localhost', port=5000):
        super().__init__()
        self.host = host
        self.port = port

    def emit(self, record):
        try:
            log_entry = self.format(record)
            with socket.create_connection((self.host, self.port)) as sock:
                sock.sendall((log_entry + "\n").encode('utf-8'))
        except Exception as e:
            logging.getLogger(__name__).error(f"Failed to send log to Logstash: {e}")
