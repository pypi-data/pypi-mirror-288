import unittest
import json
from exception_logger.app import create_app

class TestExceptionLogger(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_log_exception(self):
        response = self.client.post(
            '/log_exception',
            headers={'API-Key': 'your_api_key'},
            data=json.dumps({
                'message': 'Test error message',
                'stack_trace': 'Test stack trace'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Exception logged successfully', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
