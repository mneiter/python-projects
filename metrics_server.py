from prometheus_client import start_http_server, Counter
import time
import random

# Создаём метрику: счетчик обработанных сообщений
MESSAGES_PRODUCED = Counter('messages_produced_total', 'Total number of messages produced')

def simulate_message_production():
    while True:
        # Увеличиваем счётчик на случайное значение от 1 до 3
        MESSAGES_PRODUCED.inc(random.randint(1, 3))
        print("Produced message")
        time.sleep(2)

if __name__ == "__main__":
    # Запускаем сервер метрик на 8000 порту
    start_http_server(8000)
    print("✅ Metrics available on http://localhost:8000/metrics")

    # Имитация генерации сообщений
    simulate_message_production()
