from unittest import TestCase
from unittest.mock import MagicMock, patch
from app import KafkaApp

class TestKafkaApp(TestCase):
    @patch('app.KafkaProducerService')
    @patch('app.time.sleep', side_effect=InterruptedError)
    @patch('app.time.strftime', return_value="mocked-time")
    def test_run_producer(self, mock_strftime, mock_sleep, MockKafkaProducerService):
        mock_producer_service = MockKafkaProducerService.return_value
        app = KafkaApp(duration=5)
        app.stop_event = MagicMock(is_set=MagicMock(side_effect=[False, True]))  # Simulate one loop iteration

        with self.assertRaises(InterruptedError):  # Expecting the simulated interruption
            app.run_producer()

        mock_producer_service.send_message.assert_called_once_with({
            'number': 0,
            'timestamp': "mocked-time"  # Timestamp format is dynamic
        })
        mock_producer_service.close.assert_called_once()