import json
import logging
import time
from kafka import KafkaProducer
from config import BOOTSTRAP_SERVERS, TOPIC
from logger import get_logger
from monitoring.metrics import MESSAGES_PRODUCED


class KafkaProducerService:
    def __init__(self, logger=None):
        try:
            self.logger = logger or get_logger(self.__class__.__name__)        
            self.logger.info(f"BOOTSTRAP_SERVERS: {BOOTSTRAP_SERVERS}")
            self.producer = KafkaProducer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            self.logger.info("Kafka: Producer initialized successfully.")
        except Exception as e:
            logging.error(f"Kafka: Error initializing producer: {e}")
            raise

    def send_message(self, message: dict):
        try:
            self.producer.send(TOPIC, value=message)
            MESSAGES_PRODUCED.inc()

            self.logger.info(f"Kafka: Message sent to topic '{TOPIC}' with value: {json.dumps(message)}")
        except Exception as e:
            self.logger.error(f"Kafka: Error sending message: {e}")

    def close(self):
        self.producer.flush()
        self.producer.close()
        self.logger.info("Kafka: Producer closed.")