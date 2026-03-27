import joblib
import numpy as np
import os
from typing import Dict

class CarbonPredictor:
    def __init__(self, model_path='agbp_model.pkl'):
        # Get the absolute path to the model file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        full_model_path = os.path.join(base_dir, model_path.replace('/', os.sep))
        
        if not os.path.exists(full_model_path):
            raise FileNotFoundError(f"Model file not found at {full_model_path}")
            
        self.model = joblib.load(full_model_path)
        self.feature_names = [
            'red_band', 'green_band', 'blue_band', 'nir_band', 'swir_band',
            'ndvi', 'soil_moisture', 'temperature', 'precipitation',
            'latitude', 'longitude'
        ]
    
    def predict(self, satellite_data: Dict) -> Dict:
        """
        Input: Dict with satellite bands, soil data, climate, location
        Output: Dict with CO2 prediction, confidence interval, model hash
        """
        # Extract features in order
        features = np.array([satellite_data.get(f, 0) for f in self.feature_names])
        
        # Make prediction
        co2_tons = self.model.predict(features.reshape(1, -1))[0]
        
        # Confidence interval (±5% for MVP)
        confidence = 5.0
        lower_bound = co2_tons * (1 - confidence/100)
        upper_bound = co2_tons * (1 + confidence/100)
        
        return {
            'co2_tons': round(float(co2_tons), 2),
            'lower_bound': round(float(lower_bound), 2),
            'upper_bound': round(float(upper_bound), 2),
            'confidence_percent': float(confidence),
            'model_version': '1.0',
        }

if __name__ == "__main__":
    # Test the predictor
    predictor = CarbonPredictor()
    test_data = {
        'red_band': 100,
        'green_band': 120,
        'blue_band': 90,
        'nir_band': 200,
        'swir_band': 150,
        'ndvi': 0.7,
        'soil_moisture': 60,
        'temperature': 22,
        'precipitation': 150,
        'latitude': 0,
        'longitude': 0,
    }

    result = predictor.predict(test_data)
    print(f"Prediction: {result['co2_tons']} tons CO2/ha (±{result['confidence_percent']}%)")

