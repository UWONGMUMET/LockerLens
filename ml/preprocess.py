from __future__ import annotations

import re

import pandas as pd

TEXT_COLUMNS = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits",
    "employment_type",
    "required_experience",
    "required_education",
    "industry",
    "function",
]

def clean_text(value: object) -> str:
    text = "" if pd.isna(value) else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[^A-Za-z0-9À-ÿ.,;:!?/()@%+\-\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()

def build_training_frame(raw: pd.DataFrame) -> pd.DataFrame:
    if "fraudulent" not in raw.columns:
        raise ValueError("Dataset harus memiliki kolom 'fraudulent' sebagai label.")

    frame = raw.copy()
    available_text_columns = [column for column in TEXT_COLUMNS if column in frame.columns]
    if not available_text_columns:
        raise ValueError("Dataset tidak memiliki kolom teks yang didukung.")

    frame["combined_text"] = (
        frame[available_text_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .map(clean_text)
    )
    frame["label"] = frame["fraudulent"].astype(int)
    return frame[["combined_text", "label"]].dropna()
