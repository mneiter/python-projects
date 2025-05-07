import logging
import socket
import json
from datetime import datetime

LOGSTASH_HOST = 'localhost'
LOGSTASH_PORT = 5000

class LogstashTCPHandler(logging.Handler):
    def emit(self, record):
        try:
            log_entry = self.format(record)
            with socket.create_connection((LOGSTASH_HOST, LOGSTASH_PORT)) as sock:
                sock.sendall((log_entry + "\n").encode('utf-8'))
        except Exception as e:
            print(f"Failed to send log to Logstash: {e}")

logger = logging.getLogger("LogstashTest")
logger.setLevel(logging.INFO)

handler = LogstashTCPHandler()
handler.setFormatter(logging.Formatter(json.dumps({
    "timestamp": "%(asctime)s",
    "level": "%(levelname)s",
    "logger": "%(name)s",
    "message": "%(message)s",
    "test": "logstash test",
    "time": datetime.now().isoformat()
})))

logger.addHandler(handler)

# 🔽 TEST MESSAGE
logger.info("This is a test log message from logstash_test.py")
