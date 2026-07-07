from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from data_loader import load_fake_job_dataset
from preprocess import build_training_frame

ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "lokerlens_baseline.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"

def train() -> dict[str, float]:
    raw = load_fake_job_dataset()
    frame = build_training_frame(raw)

    x_train, x_test, y_train, y_test = train_test_split(
        frame["combined_text"],
        frame["label"],
        test_size=0.2,
        random_state=42,
        stratify=frame["label"],
    )

    model = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(max_features=30000, ngram_range=(1, 2), min_df=2)),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions, zero_division=0),
        "recall": recall_score(y_test, predictions, zero_division=0),
        "f1": f1_score(y_test, predictions, zero_division=0),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
    }

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics

if __name__ == "__main__":
    trained_metrics = train()
    print(json.dumps(trained_metrics, indent=2))
