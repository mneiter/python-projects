import threading
import time
import json
import logging
from kafka import KafkaProducer, KafkaConsumer
import redis

# Configure logging to output to both console and file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(threadName)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("logs/kafka_logs.log"),
        logging.StreamHandler()
    ]
)

# Kafka configuration
TOPIC = 'test-topic'
BOOTSTRAP_SERVERS = 'localhost:9092'
DURATION = 10  # Duration in seconds

# Redis configuration
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Event to signal threads to stop
stop_event = threading.Event()

def create_producer():
    """Create and return a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer():
    """Create and return a Kafka consumer."""
    return KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

def create_redis_client():
    """Create and return a Redis client."""
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def run_producer():
    """Function to run the Kafka producer."""
    producer = create_producer()
    try:
        i = 0
        while not stop_event.is_set():
            message = {'number': i, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}
            producer.send(TOPIC, value=message)
            logging.info(f"[Producer] Sent: {message}")
            i += 1
            time.sleep(1)
    except Exception as e:
        logging.error(f"[Producer] Error: {e}")
    finally:
        producer.flush()
        producer.close()
        logging.info("[Producer] Stopped.")

def run_consumer():
    """Function to run the Kafka consumer."""
    consumer = create_consumer()
    redis_client = create_redis_client()
    try:
        while not stop_event.is_set():
            msg_pack = consumer.poll(timeout_ms=1000)
            for messages in msg_pack.values():
                for message in messages:
                    logging.info(f"[Consumer] Received: {message.value}")
                    # Store message in Redis
                    key = f"message:{message.offset}"
                    redis_client.set(key, json.dumps(message.value))
                    logging.info(f"[Consumer] Stored in Redis with key: {key}")
    except Exception as e:
        logging.error(f"[Consumer] Error: {e}")
    finally:
        consumer.close()
        logging.info("[Consumer] Stopped.")

def main():
    """Main function to start producer and consumer threads."""
    producer_thread = threading.Thread(target=run_producer, name="ProducerThread", daemon=True)
    consumer_thread = threading.Thread(target=run_consumer, name="ConsumerThread", daemon=True)

    producer_thread.start()
    consumer_thread.start()

    try:
        time.sleep(DURATION)
    except KeyboardInterrupt:
        logging.info("[Main] Interrupted by user.")
    finally:
        logging.info(f"[Main] {DURATION} seconds elapsed. Stopping threads...")
        stop_event.set()
        producer_thread.join()
        consumer_thread.join()
        logging.info("[Main] All threads stopped.")

if __name__ == "__main__":
    main()
