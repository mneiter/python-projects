# logger.py

import logging
import os
import json
from datetime import datetime
from config import LOGSTASH_HOST, LOGSTASH_PORT, LOG_DIR

# Создаём директорию логов, если её нет
os.makedirs(LOG_DIR, exist_ok=True)

# Название файла с временной меткой
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(LOG_DIR, f"log_{timestamp}.log")

# Настройка логгера
logger = logging.getLogger("AppLogger")
logger.setLevel(logging.INFO)

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

# --- Logstash handler ---
try:
    import socket

    class LogstashTCPHandler(logging.Handler):
        def emit(self, record):
            try:
                log_entry = self.format(record)
                with socket.create_connection((LOGSTASH_HOST, LOGSTASH_PORT)) as sock:
                    sock.sendall((log_entry + "\n").encode('utf-8'))
            except Exception as e:
                logger = logging.getLogger("LogstashTCPHandler")
                logger.error(f"Failed to send log to Logstash: {e}")

    logstash_handler = LogstashTCPHandler()
    logstash_handler.setFormatter(logging.Formatter(json.dumps({
        "timestamp": "%(asctime)s",
        "level": "%(levelname)s",
        "message": "%(message)s",
        "logger": "%(name)s",
        "thread": "%(threadName)s"
    })))

    logger.addHandler(logstash_handler)

except Exception as e:
    logger.warning("Logstash handler not configured: %s", e)

# Добавляем все обработчики
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger(name="AppLogger"):
    return logging.getLogger(name)
