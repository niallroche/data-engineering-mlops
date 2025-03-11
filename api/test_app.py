import unittest
import json
import os
import sys
from unittest.mock import patch

# Set USE_DATABASE to false before importing app
os.environ['USE_DATABASE'] = 'false'

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        # Set test configuration
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('requests.post')  # Fix: mock the requests module directly
    def test_predict_endpoint(self, mock_post):
        # Mock the model service response
        mock_post.return_value.json.return_value = {"prediction": 1}
        mock_post.return_value.status_code = 200

        test_data = {
            "features": [5.1, 3.5, 1.4, 0.2]
        }
        response = self.app.post('/predict',
                               data=json.dumps(test_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('prediction', data)

if __name__ == '__main__':
    unittest.main()