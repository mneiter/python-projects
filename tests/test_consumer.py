import unittest
from unittest.mock import patch, MagicMock
from consumer import KafkaConsumerService
import threading

class TestKafkaConsumerService(unittest.TestCase):

    def setUp(self):
        # Patch Redis
        self.redis_patcher = patch('consumer.redis.Redis')
        mock_redis_class = self.redis_patcher.start()
        self.mock_redis_client = MagicMock()
        mock_redis_class.return_value = self.mock_redis_client

        # Patch KafkaConsumer
        self.kafka_patcher = patch('consumer.KafkaConsumer')
        mock_kafka_consumer_class = self.kafka_patcher.start()
        self.mock_kafka_consumer = MagicMock()
        mock_kafka_consumer_class.return_value = self.mock_kafka_consumer

        # Create instance under test
        self.kafka_consumer_service = KafkaConsumerService()

    def tearDown(self):
        self.redis_patcher.stop()
        self.kafka_patcher.stop()

    def test_consume_messages_stores_in_redis(self):
        mock_message = MagicMock()
        mock_message.value = {"key": "value"}
        mock_message.offset = 1

        self.mock_kafka_consumer.poll.return_value = {
            None: [mock_message]
        }

        stop_event = MagicMock()
        stop_event.is_set.side_effect = [False, True]  # Run one loop iteration

        self.kafka_consumer_service.consume_messages(stop_event)

        self.mock_redis_client.set.assert_called_once_with(
            "message:1", '{"key": "value"}'
        )


    def test_consume_messages_logs_error_on_exception(self):
        self.mock_kafka_consumer.poll.side_effect = Exception("Test exception")

        stop_event = MagicMock()
        stop_event.is_set.side_effect = [False, True]  # One loop iteration

        with self.assertLogs(self.kafka_consumer_service.logger, level='ERROR') as log:
            self.kafka_consumer_service.consume_messages(stop_event)

        self.assertTrue(any("Error consuming messages: Test exception" in entry for entry in log.output))

    def test_consumer_closes_on_exit(self):
        stop_event = MagicMock()
        stop_event.is_set.side_effect = [True]  # skip loop entirely

        self.kafka_consumer_service.consume_messages(stop_event)

        self.mock_kafka_consumer.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
