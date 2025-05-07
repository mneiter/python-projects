from kafka_app import KafkaApp
from logger import get_logger

if __name__ == "__main__":
    logger = get_logger("KafkaApp")
    logger.info("Starting KafkaApp from app.py")

    app = KafkaApp(logger=logger)
    app.start()
