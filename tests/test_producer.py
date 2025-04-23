from unittest import TestCase
from unittest.mock import patch, MagicMock
from producer import KafkaProducerService
from config import TOPIC

class TestKafkaProducerService(TestCase):

    @patch('producer.KafkaProducer')
    def test_send_message_success(self, mock_kafka_producer):
        # Arrange
        mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = mock_producer_instance
        service = KafkaProducerService()
        message = {"key": "value"}

        # Act + Assert
        with self.assertLogs(service.logger, level='INFO') as log:
            service.send_message(message)

        mock_producer_instance.send.assert_called_once_with(TOPIC, value=message)
        self.assertTrue(any("Sent: {'key': 'value'}" in entry for entry in log.output))

    @patch('producer.KafkaProducer')
    def test_send_message_failure(self, mock_kafka_producer):
        # Arrange
        mock_producer_instance = MagicMock()
        mock_producer_instance.send.side_effect = Exception("Test exception")
        mock_kafka_producer.return_value = mock_producer_instance
        service = KafkaProducerService()
        message = {"key": "value"}

        # Act + Assert
        with self.assertLogs(service.logger, level='ERROR') as log:
            service.send_message(message)

        self.assertTrue(any("Error sending message: Test exception" in entry for entry in log.output))
