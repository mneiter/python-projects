import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()

# Logging setup (early so we can use it during config validation)
LOG_DIR = 'logs'
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_FILE = f'log_{timestamp}.log'

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

# Helper to validate required env vars
def get_env_or_fail(var_name, default=None, required=False):
    value = os.getenv(var_name, default)
    if required and not value:
        logger.error(f"Missing required environment variable: {var_name}")
        raise EnvironmentError(f"Missing required env variable: {var_name}")
    return value

# Kafka configuration
TOPIC = get_env_or_fail("TOPIC", "test-topic")
BOOTSTRAP_SERVERS = get_env_or_fail("BOOTSTRAP_SERVERS", required=True)
GROUP_ID = get_env_or_fail("GROUP_ID", "my-group")

# Redis configuration
REDIS_HOST = get_env_or_fail("REDIS_HOST", "localhost")
REDIS_PORT = int(get_env_or_fail("REDIS_PORT", 6379))
REDIS_DB = int(get_env_or_fail("REDIS_DB", 0))

# MongoDB configuration
MONGODB_URI = get_env_or_fail("MONGODB_URI", required=True)

# Duration
DURATION = int(get_env_or_fail("DURATION", 60))

# Log the config summary
logger.info(f"Kafka: {BOOTSTRAP_SERVERS}, Topic: {TOPIC}, Group: {GROUP_ID}")
logger.info(f"Redis: {REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
logger.info(f"MongoDB: {MONGODB_URI}")
