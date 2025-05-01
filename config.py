import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Environment type ---
ENVIRONMENT = os.getenv("ENVIRONMENT", "local").lower()
IS_DOCKER = ENVIRONMENT == "docker"

# --- Kafka ---
TOPIC = os.getenv("TOPIC", "test-topic")
GROUP_ID = os.getenv("GROUP_ID", "my-group")
BOOTSTRAP_SERVERS = os.getenv(
    "BOOTSTRAP_SERVERS",
    "kafka:19092" if IS_DOCKER else "localhost:9092"
)

# --- Redis ---
REDIS_HOST = os.getenv("REDIS_HOST", "redis" if IS_DOCKER else "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# --- MongoDB ---
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    "mongodb://mongo-db:27017" if IS_DOCKER else "mongodb://localhost:27017"
)

# --- Elasticsearch ---
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "elasticsearch" if IS_DOCKER else "localhost")
ELASTICSEARCH_PORT = int(os.getenv("ELASTICSEARCH_PORT", 9200))
ELASTICSEARCH_SCHEME = os.getenv("ELASTICSEARCH_SCHEME", "http")
ELASTICSEARCH_LOG_INDEX = os.getenv("ELASTICSEARCH_LOG_INDEX", "logs-app")

# --- Logstash Config ---
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "logstash" if IS_DOCKER else "localhost")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", 5000))

# --- Runtime ---
DURATION = int(os.getenv("DURATION", 60))

# --- Logging ---
LOG_DIR = "logs"
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

# --- Startup log summary ---
logger.info(f"[ENV] Running in {'DOCKER' if IS_DOCKER else 'LOCAL'} mode")
logger.info(f"Kafka: {BOOTSTRAP_SERVERS}, Topic: {TOPIC}, Group: {GROUP_ID}")
logger.info(f"Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
logger.info(f"MongoDB: {MONGODB_URI}")
logger.info(f"Elasticsearch: {ELASTICSEARCH_SCHEME}://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}")
logger.info(f"Logstash: {LOGSTASH_HOST}:{LOGSTASH_PORT}")
