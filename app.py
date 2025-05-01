import json
import threading
import time
import logging
from producer import KafkaProducerService
from consumer import KafkaConsumerService
from mongodb_consumer import MongoDBConsumerService
from config import DURATION, LOGSTASH_HOST, LOGSTASH_PORT
from handlers.logstash_handler import LogstashTCPHandler

class KafkaApp:
    def __init__(self, duration=DURATION):
        self.duration = duration
        self.stop_event = threading.Event()       

        self.initialize_logger()

        self.producer_service = KafkaProducerService()
        self.consumer_service = KafkaConsumerService()
        self.mongo_consumer_service = MongoDBConsumerService() 

    def initialize_logger(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
        
        self.logstash_handler = LogstashTCPHandler(host=LOGSTASH_HOST, port=LOGSTASH_PORT)
        formatter = logging.Formatter(json.dumps({
            "timestamp": "%(asctime)s",
            "level": "%(levelname)s",
            "message": "%(message)s",
            "logger": "%(name)s",
            "thread": "%(threadName)s"
        }))
        self.logstash_handler.setFormatter(formatter)
        self.logger.addHandler(self.logstash_handler)       

    def run_producer(self):
        i = 0
        try:
            while not self.stop_event.is_set():
                message = {'number': i, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')}
                self.producer_service.send_message(message)
                i += 1
                time.sleep(1)
        finally:
            self.producer_service.close()

    def run_consumer(self):
        self.consumer_service.consume_messages(self.stop_event)

    def run_mongo_consumer(self):
        self.mongo_consumer_service.consume_mongodb_examples()
        self.mongo_consumer_service.consume_documents(self.stop_event)

    def start(self):
        producer_thread = threading.Thread(target=self.run_producer, name="ProducerThread", daemon=True)
        consumer_thread = threading.Thread(target=self.run_consumer, name="ConsumerThread", daemon=True)
        mongo_consumer_thread = threading.Thread(target=self.run_mongo_consumer, name="MongoDBConsumerThread", daemon=True)

        producer_thread.start()
        consumer_thread.start()
        mongo_consumer_thread.start()

        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user.")
        finally:
            self.logger.info(f"{self.duration} seconds elapsed. Stopping threads...")
            self.stop_event.set()
            producer_thread.join()
            consumer_thread.join()
            mongo_consumer_thread.join()
            self.logger.info("All threads stopped.")

if __name__ == "__main__":
    app = KafkaApp(duration=DURATION)
    app.start()
