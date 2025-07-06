# backend/ml.py

import joblib
import os

# Load model once
model_path = os.path.join(os.path.dirname(__file__), "ml_models", "wait_predictor.pkl")
wait_model = joblib.load(model_path)

def predict_wait_time(features: list):
    prediction = wait_model.predict([features])[0]
    return round(prediction)