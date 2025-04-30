import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env (if present)
load_dotenv()

# --- Detect environment: local or docker ---
ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()

IS_DOCKER = ENVIRONMENT == "docker"

# --- Kafka configuration ---
TOPIC = os.getenv("TOPIC", "test-topic")
BOOTSTRAP_SERVERS = os.getenv(
    "BOOTSTRAP_SERVERS",
    "kafka:9092" if IS_DOCKER else "localhost:9092"
)
GROUP_ID = os.getenv("GROUP_ID", "my-group")

# --- Redis configuration ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis" if IS_DOCKER else "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# --- MongoDB configuration ---
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://mongo-db:27017" if IS_DOCKER else "mongodb://localhost:27017"
)

# --- Runtime ---
DURATION = int(os.getenv("DURATION", 60))

# --- Logging setup ---
LOG_DIR = 'logs'
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f"log_{timestamp}.log"

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

logger = logging.getLogger("Config")

# --- Output config summary ---
logger.info(f"[ENV] Running in {'DOCKER' if IS_DOCKER else 'LOCAL'} mode")
logger.info(f"Kafka: {BOOTSTRAP_SERVERS}, Topic: {TOPIC}, Group: {GROUP_ID}")
logger.info(f"Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
logger.info(f"MongoDB: {MONGODB_URI}")