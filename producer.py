import json
import logging
import time
from kafka import KafkaProducer
from config import BOOTSTRAP_SERVERS, TOPIC

class KafkaProducerService:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_message(self, message: dict):
        try:
            self.producer.send(TOPIC, value=message)
            self.logger.info(f"Kafka: Message sent to topic '{TOPIC}' with value: {json.dumps(message)}")
        except Exception as e:
            self.logger.error(f"Kafka: Error sending message: {e}")

    def close(self):
        self.producer.flush()
        self.producer.close()
        self.logger.info("Kafka: Producer closed.")