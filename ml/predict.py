from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib

from preprocess import clean_text

MODEL_PATH = Path(__file__).resolve().parent / "artifacts" / "lokerlens_baseline.joblib"

def predict_text(text: str) -> dict:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model belum tersedia. Jalankan python ml/train_model.py terlebih dahulu.")

    model = joblib.load(MODEL_PATH)
    cleaned = clean_text(text)
    prediction = int(model.predict([cleaned])[0])
    probability = model.predict_proba([cleaned])[0].tolist() if hasattr(model, "predict_proba") else []
    return {
        "risk_label": "higher_risk" if prediction == 1 else "lower_risk",
        "fraud_probability": probability[1] if len(probability) > 1 else None,
    }

if __name__ == "__main__":
    input_text = " ".join(sys.argv[1:]).strip()
    if not input_text:
        raise SystemExit('Usage: python ml/predict.py "job posting text"')
    print(json.dumps(predict_text(input_text), indent=2))
