import logging
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from config import LOGSTASH_HOST, LOGSTASH_PORT, LOG_DIR

# Load environment variables
load_dotenv()

# Logging output configuration from .env
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "true").lower() == "true"
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
LOG_TO_LOGSTASH = os.getenv("LOG_TO_LOGSTASH", "true").lower() == "true"

LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "localhost")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", 5000))

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Timestamped log file name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(LOG_DIR, f"log_{timestamp}.log")

# Create base logger
_logger = logging.getLogger("AppLogger")
_logger.setLevel(logging.INFO)

# --- File handler ---
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# --- Console handler ---
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
))

# --- Logstash TCP handler ---
class LogstashTCPHandler(logging.Handler):
    def emit(self, record):
        try:
            import socket
            log_entry = self.format(record)
            with socket.create_connection((LOGSTASH_HOST, LOGSTASH_PORT)) as sock:
                sock.sendall((log_entry + "\n").encode('utf-8'))
        except Exception as e:
            fallback_logger = logging.getLogger("LogstashTCPHandler")
            fallback_logger.warning(f"Failed to send log to Logstash: {e}")

# Attach handlers based on environment settings
if LOG_TO_FILE:
    _logger.addHandler(file_handler)

if LOG_TO_CONSOLE:
    _logger.addHandler(console_handler)

if LOG_TO_LOGSTASH:
    try:
        logstash_formatter = logging.Formatter(json.dumps({
            "timestamp": "%(asctime)s",
            "level": "%(levelname)s",
            "message": "%(message)s",
            "logger": "%(name)s",
            "thread": "%(threadName)s"
        }))
        logstash_handler = LogstashTCPHandler()
        logstash_handler.setFormatter(logstash_formatter)
        _logger.addHandler(logstash_handler)
    except Exception as e:
        _logger.warning("Logstash handler not configured: %s", e)

_logger.info("This is a test log message from logger.py")

# Getter to reuse logger elsewhere
def get_logger(name="AppLogger"):
    logger = logging.getLogger(name)
    if not logger.handlers:  # Avoid duplicate handlers
        for handler in _logger.handlers:
            logger.addHandler(handler)
        logger.setLevel(_logger.level)
    return logger
