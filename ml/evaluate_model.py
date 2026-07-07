from __future__ import annotations

import json
from pathlib import Path

METRICS_PATH = Path(__file__).resolve().parent / "artifacts" / "metrics.json"

def load_metrics() -> dict:
    if not METRICS_PATH.exists():
        raise FileNotFoundError("Belum ada metrics.json. Jalankan python ml/train_model.py terlebih dahulu.")
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))

if __name__ == "__main__":
    print(json.dumps(load_metrics(), indent=2))
