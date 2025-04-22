import threading
import time
import json
from kafka import KafkaProducer, KafkaConsumer

TOPIC = 'test-topic'
BOOTSTRAP_SERVERS = 'localhost:9092'
DURATION = 20  # Время работы в секундах

# Флаг для управления завершением потоков
stop_event = threading.Event()

def run_producer():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    i = 0
    while not stop_event.is_set():
        message = {'number': i, 'timestamp': time.time()}
        producer.send(TOPIC, value=message)
        print(f"[Producer] Sent: {message}")
        i += 1
        time.sleep(1)
    producer.flush()
    producer.close()
    print("[Producer] Завершение работы.")

def run_consumer():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    while not stop_event.is_set():
        msg_pack = consumer.poll(timeout_ms=1000)
        for tp, messages in msg_pack.items():
            for message in messages:
                print(f"[Consumer] Received: {message.value}")
    consumer.close()
    print("[Consumer] Завершение работы.")

if __name__ == "__main__":
    # Запуск потоков продюсера и консюмера
    producer_thread = threading.Thread(target=run_producer)
    consumer_thread = threading.Thread(target=run_consumer)

    consumer_thread.start()
    producer_thread.start()

    # Ожидание заданного времени
    time.sleep(DURATION)
    print(f"[Main] Прошло {DURATION} секунд. Завершение работы...")

    # Установка флага завершения
    stop_event.set()

    # Ожидание завершения потоков
    producer_thread.join()
    consumer_thread.join()

    print("[Main] Все потоки завершены.")
