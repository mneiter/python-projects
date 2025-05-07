from kafka_app import KafkaApp
from logger import get_logger
from monitoring.metrics import start_metrics_server

if __name__ == "__main__":
    logger = get_logger("KafkaApp")
    logger.info("Starting KafkaApp from app.py")

    start_metrics_server(port=8000)

    app = KafkaApp(logger=logger)
    app.start()
