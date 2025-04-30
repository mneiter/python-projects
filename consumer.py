import json
import logging
from kafka import KafkaConsumer
import redis
from services.mongodb_service import MongoDBService
from config import BOOTSTRAP_SERVERS, TOPIC, GROUP_ID, REDIS_HOST, REDIS_PORT, REDIS_DB

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            TOPIC,
            bootstrap_servers='localhost:9092',
            # bootstrap_servers=BOOTSTRAP_SERVERS,
            auto_offset_reset='earliest',
            group_id=GROUP_ID,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        self.mongo_service = MongoDBService()
        self.logger = logging.getLogger(self.__class__.__name__)

    def consume_messages(self, stop_event):
        try:
            while not stop_event.is_set():
                msg_pack = self.consumer.poll(timeout_ms=1000)
                for messages in msg_pack.values():
                    for message in messages:
                        self.logger.info(f"Received: {message.value}")
                        key = f"message:{message.offset}"
                        # Store in Redis with a TTL of 1 day
                        # Using message offset as the key for Redis
                        self.redis_client.set(key, json.dumps(message.value), ex=60*60*24) 
                        self.logger.info(f"Stored in Redis with key: {key}")
                        # Store in MongoDB
                        # Using message value as the document to be stored in MongoDB
                        self.mongo_service.insert_document('kafka_messages', message.value)
                        self.logger.info(f"Stored in MongoDB in collection 'kafka_messages'")
        except Exception as e:
            self.logger.error(f"Error consuming messages: {e}")
        finally:
            self.consumer.close()
            self.logger.info("Consumer closed.")