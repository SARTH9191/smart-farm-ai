# agents/lead_agent.py
import os
import time
import pandas as pd
import joblib
import requests
from datetime import datetime

MODEL_PATH = "models/lead_agent_model.pkl"
SOIL_CSV = "data/soil_data.csv"
LEAD_ENDPOINT = "http://127.0.0.1:8000/lead/decision"
POLL_INTERVAL = 5

def load_model():
    d = joblib.load(MODEL_PATH)
    return d["model"], d["features"]

def get_latest_row():
    df = pd.read_csv(SOIL_CSV, parse_dates=["timestamp"])
    return df.sort_values("timestamp").iloc[-1:]

def predict_and_send(model, features):
    row = get_latest_row()
    X = row[features].fillna(0)
    pred = model.predict(X)[0]
    proba = model.predict_proba(X).max(axis=1)[0]

    payload = {
        "decision": pred,
        "confidence": float(proba),
        "timestamp": datetime.utcnow().isoformat(),
        "source": "lead_agent"
    }
    print("Predicted:", payload)
    try:
        r = requests.post(LEAD_ENDPOINT, json=payload, timeout=5)
        print("Posted to FastAPI:", r.status_code)
    except Exception as e:
        print("Failed to send:", e)

if __name__ == "__main__":
    model, features = load_model()
    while True:
        predict_and_send(model, features)
        time.sleep(POLL_INTERVAL)

