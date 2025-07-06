# train_model_local.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

np.random.seed(42)
num_samples = 300

data = {
    "age": np.random.randint(10, 80, size=num_samples),
    "gender": np.random.choice([0, 1], size=num_samples),
    "problem_code": np.random.randint(1, 6, size=num_samples),
    "queue_length": np.random.randint(1, 15, size=num_samples),
    "hour": np.random.randint(8, 18, size=num_samples),
}

data["wait_time"] = (
    data["queue_length"] * 4
    + data["problem_code"] * 2
    + data["age"] * 0.1
    + np.random.normal(0, 3, size=num_samples)
).round().astype(int)

df = pd.DataFrame(data)

X = df[["age", "gender", "problem_code", "queue_length", "hour"]]
y = df["wait_time"]

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model locally using your sklearn version
joblib.dump(model, "backend/ml_models/wait_predictor.pkl")
print("✅ Model trained and saved!")
