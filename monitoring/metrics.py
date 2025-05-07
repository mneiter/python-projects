from prometheus_client import Counter, Histogram, start_http_server
import time

# --- Define Prometheus metrics ---
MESSAGES_PRODUCED = Counter('kafka_messages_produced_total', 'Total messages produced to Kafka')
MESSAGES_CONSUMED = Counter('kafka_messages_consumed_total', 'Total messages consumed from Kafka')
MESSAGE_PROCESSING_TIME = Histogram('kafka_message_processing_seconds', 'Time spent processing message')

def start_metrics_server(port=8000):
    start_http_server(port)
    print(f"Prometheus metrics server started on port {port}")
