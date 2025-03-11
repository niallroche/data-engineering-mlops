import unittest
import os
import joblib
import numpy as np

class TestModel(unittest.TestCase):
    def setUp(self):
        # Ensure the model file exists before tests run.
        self.model_path = "model/logistic_model.pkl"
        self.assertTrue(os.path.exists(self.model_path), "Model file not found. Have you run train_model.py?")
        self.model = joblib.load(self.model_path)
    
    def test_prediction(self):
        # Test a sample prediction
        input_features = [5.1, 3.5, 1.4, 0.2]
        prediction = self.model.predict([input_features])
        # Check that the prediction is an integer type (e.g. one of the iris target labels)
        self.assertTrue(isinstance(prediction[0], (int, np.integer)), "Prediction should be an integer")
        
        # Optionally, you could check that the prediction is within expected class labels (for iris: 0, 1, or 2)
        self.assertIn(prediction[0], [0, 1, 2], "Prediction is not within expected class labels")
        
if __name__ == '__main__':
    unittest.main()