import logging
import os
from datetime import datetime

# Kafka configuration
TOPIC = 'test-topic'
BOOTSTRAP_SERVERS = 'localhost:9092'
GROUP_ID = 'my-group'

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Duration in seconds
DURATION = 60  

# Logging configuration
LOG_DIR = 'logs'

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f'kafka_logs_{timestamp}.log'

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, LOG_FILE)),
        logging.StreamHandler()
    ]
)