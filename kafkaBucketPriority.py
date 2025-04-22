import threading
import time
import json
import logging
from kafka import KafkaProducer, KafkaConsumer, TopicPartition

# Configure logging
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
BOOTSTRAP_SERVERS = 'localhost:9092'
DURATION = 10  # Duration in seconds

# Topics for different priorities
HIGH_PRIORITY_TOPIC = 'high-priority'
LOW_PRIORITY_TOPIC = 'low-priority'

# Event to signal threads to stop
stop_event = threading.Event()

def create_producer():
    """Create and return a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def create_consumer(topics):
    """Create and return a Kafka consumer subscribed to specified topics."""
    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='priority-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    consumer.subscribe(topics)
    return consumer

def run_producer():
    """Function to run the Kafka producer."""
    producer = create_producer()
    try:
        i = 0
        while not stop_event.is_set():
            # Alternate between high and low priority messages
            if i % 2 == 0:
                topic = HIGH_PRIORITY_TOPIC
                priority = 'high'
            else:
                topic = LOW_PRIORITY_TOPIC
                priority = 'low'
            message = {'number': i, 'priority': priority, 'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}
            producer.send(topic, value=message)
            logging.info(f"[Producer] Sent to {topic}: {message}")
            i += 1
            time.sleep(1)
    except Exception as e:
        logging.error(f"[Producer] Error: {e}")
    finally:
        producer.flush()
        producer.close()
        logging.info("[Producer] Stopped.")
        time.sleep(DURATION)

def run_consumer():
    """Function to run the Kafka consumer."""
    consumer = create_consumer([HIGH_PRIORITY_TOPIC, LOW_PRIORITY_TOPIC])
    try:
        while not stop_event.is_set():
            msg_pack = consumer.poll(timeout_ms=1000)
            # Process high priority messages first
            high_priority_messages = []
            low_priority_messages = []
            for tp, messages in msg_pack.items():
                for message in messages:
                    if message.topic == HIGH_PRIORITY_TOPIC:
                        high_priority_messages.append(message)
                    else:
                        low_priority_messages.append(message)
            for message in high_priority_messages:
                logging.info(f"[Consumer] High Priority Received: {message.value}")
            for message in low_priority_messages:
                logging.info(f"[Consumer] Low Priority Received: {message.value}")
    except Exception as e:
        logging.error(f"[Consumer] Error: {e}")
    finally:
        consumer.close()
        logging.info("[Consumer] Stopped.")
        time.sleep(DURATION)

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
