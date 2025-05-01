# kafka_app.py

import json
import threading
import time
from producer import KafkaProducerService
from consumer import KafkaConsumerService
from mongodb_consumer import MongoDBConsumerService
from config import DURATION
from logger import get_logger


class KafkaApp:
    def __init__(self, logger=None):
        try:
            self.logger = logger or get_logger(self.__class__.__name__)
            self.duration = DURATION
            self.stop_event = threading.Event()

            self.logger.info("Initializing KafkaApp...")

            self.producer_service = KafkaProducerService(logger=self.logger)
            self.consumer_service = KafkaConsumerService(logger=self.logger)
            self.mongo_consumer_service = MongoDBConsumerService(logger=self.logger)

            self.logger.info("KafkaApp initialized successfully.")
        except Exception as e:
            logger.error(f"Error during KafkaApp initialization: {e}")
            raise

    def run_producer(self):
        i = 0
        try:
            while not self.stop_event.is_set():
                message = {
                    'number': i,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                self.producer_service.send_message(message)
                i += 1
                time.sleep(1)
        except Exception as e:
            self.logger.error(f"Error in producer loop: {e}")
        finally:
            self.producer_service.close()

    def run_consumer(self):
        self.consumer_service.consume_messages(self.stop_event)

    def run_mongo_consumer(self):
        self.mongo_consumer_service.consume_mongodb_examples()
        self.mongo_consumer_service.consume_documents(self.stop_event)

    def start(self):
        self.logger.info("Starting KafkaApp threads...")

        threads = [
            threading.Thread(target=self.run_producer, name="ProducerThread", daemon=True),
            threading.Thread(target=self.run_consumer, name="ConsumerThread", daemon=True),
            threading.Thread(target=self.run_mongo_consumer, name="MongoDBConsumerThread", daemon=True),
        ]

        for t in threads:
            t.start()

        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user.")
        finally:
            self.logger.info(f"{self.duration} seconds elapsed. Stopping threads...")
            self.stop_event.set()
            for t in threads:
                t.join()
            self.logger.info("All threads stopped.")
