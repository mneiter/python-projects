import json
import logging
from kafka import KafkaConsumer
import redis
from config import BOOTSTRAP_SERVERS, TOPIC, GROUP_ID, REDIS_HOST, REDIS_PORT, REDIS_DB

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            group_id=GROUP_ID,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.logger = logging.getLogger(self.__class__.__name__)

    def consume_messages(self, stop_event):
        try:
            while not stop_event.is_set():
                msg_pack = self.consumer.poll(timeout_ms=1000)
                for messages in msg_pack.values():
                    for message in messages:
                        self.logger.info(f"Received: {message.value}")
                        key = f"message:{message.offset}"
                        self.redis_client.set(key, json.dumps(message.value))
                        self.logger.info(f"Stored in Redis with key: {key}")
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e}")
        finally:
            self.consumer.close()
            self.logger.info("Consumer closed.")