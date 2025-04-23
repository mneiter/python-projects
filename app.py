import threading
import time
import logging
from producer import KafkaProducerService
from consumer import KafkaConsumerService

class KafkaApp:
    def __init__(self, duration=60):
        self.duration = duration
        self.stop_event = threading.Event()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.producer_service = KafkaProducerService()
        self.consumer_service = KafkaConsumerService()

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

    def start(self):
        producer_thread = threading.Thread(target=self.run_producer, name="ProducerThread", daemon=True)
        consumer_thread = threading.Thread(target=self.run_consumer, name="ConsumerThread", daemon=True)

        producer_thread.start()
        consumer_thread.start()

        try:
            time.sleep(self.duration)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user.")
        finally:
            self.logger.info(f"{self.duration} seconds elapsed. Stopping threads...")
            self.stop_event.set()
            producer_thread.join()
            consumer_thread.join()
            self.logger.info("All threads stopped.")

if __name__ == "__main__":
    app = KafkaApp(duration=60)
    app.start()