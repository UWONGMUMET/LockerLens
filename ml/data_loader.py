from __future__ import annotations

import os
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = PROJECT_ROOT / "ml" / "data" / "fake_job_postings.csv"

def dataset_path() -> Path:
    return Path(os.getenv("FAKE_JOB_CSV", DEFAULT_DATASET)).expanduser().resolve()

def load_fake_job_dataset(path: str | Path | None = None) -> pd.DataFrame:
    csv_path = Path(path).expanduser().resolve() if path else dataset_path()
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset tidak ditemukan di {csv_path}. Simpan Fake Job Posting / EMSCAD CSV "
            "ke ml/data/fake_job_postings.csv atau set FAKE_JOB_CSV."
        )
    return pd.read_csv(csv_path)
