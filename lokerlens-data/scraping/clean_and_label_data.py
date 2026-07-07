import os
import re
import logging
from datetime import datetime

import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw", "scraped_job_posts.csv")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
FINAL_COLUMNS = [
    "id", "source_name", "source_platform", "source_url", "collected_at", "job_title", "company_name",
    "company_clarity", "job_type", "job_text", "job_description", "requirements", "benefits",
    "compensation_status", "compensation_text", "working_hours_status", "working_hours_text",
    "work_arrangement", "location", "duration_status", "duration_text", "contact_type",
    "asks_sensitive_data", "sensitive_data_terms", "asks_payment", "payment_terms", "unrealistic_promise",
    "unrealistic_promise_terms", "workload_status", "missing_fields", "red_flag_categories",
    "red_flag_count", "trust_score", "risk_level", "recommended_action", "notes",
]
PLATFORMS = {"linkedin", "instagram", "twitter_x", "telegram", "job_site", "company_website", "other"}
JOB_TYPES = {"internship", "freelance", "part_time", "entry_level", "unknown"}

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def clean_text(value):
    text = "" if value is None or pd.isna(value) else str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def normalize_platform(value):
    text = clean_text(value).lower().replace("-", "_").replace(" ", "_")
    aliases = {"twitter": "twitter_x", "x": "twitter_x", "remote_job_board": "job_site"}
    return aliases.get(text, text if text in PLATFORMS else "other")

def normalize_job_type(value):
    text = clean_text(value).lower().replace("-", "_").replace(" ", "_")
    if re.search(r"\b(intern|internship|magang)\b", text):
        return "internship"
    if re.search(r"\b(freelance|contractor)\b", text):
        return "freelance"
    if re.search(r"\b(part_time|parttime|part)\b", text):
        return "part_time"
    if re.search(r"\b(entry|junior|graduate|associate)\b", text):
        return "entry_level"
    return text if text in JOB_TYPES else "unknown"

def detect_company_clarity(row):
    company = clean_text(row.get("company_name", ""))
    text = f"{company} {row.get('job_text', '')}".lower()
    if company and company.lower() not in {"confidential", "unknown", "n/a", "not disclosed"}:
        return "clear"
    if re.search(r"\b(confidential|undisclosed|company not disclosed|stealth)\b", text):
        return "unclear"
    return "missing"

def detect_compensation(text):
    lowered = text.lower()
    if re.search(r"\b(komisi saja|commission based|berbasis komisi)\b", lowered):
        return "commission_only", _extract_evidence(text, r"\b(komisi saja|commission based|berbasis komisi).{0,100}")
    if re.search(r"\b(unpaid|tidak dibayar|tanpa gaji|volunteer)\b", lowered):
        return "unpaid", _extract_evidence(text, r"\b(unpaid|tidak dibayar|tanpa gaji|volunteer).{0,100}")
    if re.search(r"\b(gaji|salary|paid|uang saku|allowance|fee|honor|insentif|stipend|\$|€|rp)\b", lowered):
        return "paid", _extract_evidence(text, r"\b(gaji|salary|paid|uang saku|allowance|fee|honor|insentif|stipend|\$|€|rp).{0,120}")
    return "not_mentioned", ""

def detect_working_hours(text):
    lowered = text.lower()
    if re.search(r"\b(09\.00|17\.00|senin|jumat|jam kerja|jam/minggu|hours per week|full-time|part-time|shift|working hours)\b", lowered):
        return "clear", _extract_evidence(text, r"\b(09\.00|17\.00|senin|jumat|jam kerja|jam/minggu|hours per week|full-time|part-time|shift|working hours).{0,100}")
    if re.search(r"\b(flexible|fleksibel|bebas waktu)\b", lowered):
        return "unclear", _extract_evidence(text, r"\b(flexible|fleksibel|bebas waktu).{0,100}")
    return "not_mentioned", ""

def detect_work_arrangement(text):
    lowered = text.lower()
    if re.search(r"\bhybrid\b", lowered):
        return "hybrid"
    if re.search(r"\b(wfo|onsite|on-site|work from office)\b", lowered):
        return "wfo"
    if re.search(r"\b(wfh|remote|work from home|home office)\b", lowered):
        return "wfh"
    return "not_mentioned"

def detect_duration(text):
    lowered = text.lower()
    if re.search(r"\b(\d+\s*(month|months|bulan|week|weeks|minggu)|duration|durasi|contract|kontrak|period|periode|probation)\b", lowered):
        return "clear", _extract_evidence(text, r"\b(\d+\s*(month|months|bulan|week|weeks|minggu)|duration|durasi|contract|kontrak|period|periode|probation).{0,100}")
    if re.search(r"\b(tentative|tentatif|to be discussed|menyesuaikan)\b", lowered):
        return "unclear", _extract_evidence(text, r"\b(tentative|tentatif|to be discussed|menyesuaikan).{0,100}")
    return "not_mentioned", ""

def detect_contact_type(text):
    lowered = text.lower()
    if re.search(r"(google\.com/forms|forms\.gle|typeform|application form|form pendaftaran)", lowered):
        return "form_link"
    if "personal_email" in lowered:
        return "personal_email"
    if re.search(r"[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com", text, flags=re.I):
        return "personal_email"
    email = re.search(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
    if email:
        return "company_email"
    if "whatsapp_personal" in lowered or re.search(r"\b(whatsapp|wa\b)\b", lowered):
        return "whatsapp_personal"
    if re.search(r"\b(official website|career page|careers page|website resmi)\b", lowered):
        return "official_website"
    return "not_mentioned"

def detect_sensitive_data(text):
    patterns = {
        "sensitive_data_detected": r"\b(ktp|rekening|otp|password|kartu keluarga|foto identitas|selfie ktp|bank account|pin)\b",
    }
    terms = [name for name, pattern in patterns.items() if re.search(pattern, text.lower())]
    return ("yes" if terms else "no"), ";".join(terms)

def detect_payment_request(text):
    patterns = {"payment_request_detected": r"\b(biaya pendaftaran|deposit|admin fee|biaya admin|transfer dulu|bayar dulu|require payment)\b"}
    terms = [name for name, pattern in patterns.items() if re.search(pattern, text.lower())]
    return ("yes" if terms else "no"), ";".join(terms)

def detect_unrealistic_promise(text):
    patterns = {"unrealistic_promise_detected": r"\b(penghasilan tidak terbatas|cepat kaya|kerja mudah|gaji besar|modal kecil|langsung cuan|unlimited income)\b"}
    terms = [name for name, pattern in patterns.items() if re.search(pattern, text.lower())]
    return ("yes" if terms else "no"), ";".join(terms)

def detect_workload(text):
    lowered = text.lower()
    if re.search(r"\b(heavy workload|tight deadline|setiap hari|deadline ketat|long hours|overtime)\b", lowered):
        return "heavy"
    if re.search(r"\b(part-time|hours per week|clear scope|deliverables|balanced workload)\b", lowered):
        return "reasonable"
    return "unclear"

def detect_missing_fields(row):
    missing = []
    if row["company_clarity"] != "clear":
        missing.append("company")
    if not row["job_description"]:
        missing.append("jobdesc")
    if row["compensation_status"] == "not_mentioned":
        missing.append("compensation")
    if row["working_hours_status"] in {"not_mentioned", "unclear"}:
        missing.append("working_hours")
    if row["work_arrangement"] == "not_mentioned":
        missing.append("work_arrangement")
    if not row["location"]:
        missing.append("location")
    if row["duration_status"] in {"not_mentioned", "unclear"}:
        missing.append("duration")
    if row["contact_type"] == "not_mentioned":
        missing.append("contact")
    if not _has_pattern(row["job_text"], r"\b(contract|agreement|offer letter|kontrak|perjanjian)\b"):
        missing.append("contract")
    if not _has_pattern(row["job_text"], r"\b(deadline|closing date|apply by|batas apply|batas pendaftaran)\b"):
        missing.append("deadline")
    if not _has_pattern(row["job_text"], r"\b(supervisor|mentor|manager|report to|reports to|pic|pembimbing)\b"):
        missing.append("supervisor")
    return ";".join(missing)

def detect_red_flags(row):
    flags = []
    missing = set(_split_semicolon(row["missing_fields"]))
    if row["asks_payment"] == "yes":
        flags.append("asks_payment")
    if row["asks_sensitive_data"] == "yes":
        flags.append("asks_sensitive_data")
    if row["unrealistic_promise"] == "yes":
        flags.append("unrealistic_promise")
    if row["company_clarity"] != "clear":
        flags.append("unclear_company")
    if "compensation" in missing:
        flags.append("compensation_missing")
    if "working_hours" in missing:
        flags.append("working_hours_missing")
    if row["compensation_status"] == "unpaid" and row["workload_status"] == "heavy":
        flags.append("unpaid_heavy_workload")
    if row["contact_type"] in {"personal_email", "whatsapp_personal"}:
        flags.append("contact_unprofessional")
    if "jobdesc" in missing or _has_pattern(row["job_text"], r"\b(serabutan|mengerjakan semua|all-rounder|ambiguous role)\b"):
        flags.append("jobdesc_ambiguous")
    return ";".join(dict.fromkeys(flags))

def calculate_trust_score(row):
    score = 100
    flags = set(_split_semicolon(row["red_flag_categories"]))
    missing = set(_split_semicolon(row["missing_fields"]))
    flag_deductions = {
        "asks_payment": 30, "asks_sensitive_data": 25, "unrealistic_promise": 20, "unclear_company": 20,
        "compensation_missing": 10, "working_hours_missing": 10, "jobdesc_ambiguous": 10,
        "contact_unprofessional": 10,
    }
    missing_deductions = {"duration": 5, "contract": 5, "deadline": 3, "supervisor": 5}
    for flag, deduction in flag_deductions.items():
        if flag in flags:
            score -= deduction
    for field, deduction in missing_deductions.items():
        if field in missing:
            score -= deduction
    if missing:
        score = min(score, 95)
    if missing & {"company", "compensation", "jobdesc", "working_hours", "contact"}:
        score = min(score, 84)
    if flags & {"unrealistic_promise", "unclear_company", "unpaid_heavy_workload"}:
        score = min(score, 69)
    if flags & {"asks_payment", "asks_sensitive_data"}:
        score = min(score, 44)
    return max(0, min(100, int(score)))

def assign_risk_level(score):
    if score >= 85:
        return "Aman Dilamar"
    if score >= 70:
        return "Cukup Aman, Tapi Perlu Dicek"
    if score >= 45:
        return "Berisiko Sedang"
    return "Risiko Tinggi"

def assign_recommended_action(risk_level):
    actions = {
        "Aman Dilamar": "Apply",
        "Cukup Aman, Tapi Perlu Dicek": "Apply setelah klarifikasi",
        "Berisiko Sedang": "Jangan apply dulu sebelum verifikasi",
        "Risiko Tinggi": "Hindari atau verifikasi secara ketat",
    }
    return actions[risk_level]

def build_labeled_dataset():
    if not os.path.exists(RAW_PATH):
        raise FileNotFoundError(f"Raw dataset not found: {RAW_PATH}")
    raw = pd.read_csv(RAW_PATH).fillna("")
    rows = []
    for index, row in raw.iterrows():
        rows.append(_label_record(row, index + 1))
    return pd.DataFrame(rows, columns=FINAL_COLUMNS)

def save_outputs(df):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)
    clean_columns = [column for column in FINAL_COLUMNS if column not in {"trust_score", "risk_level", "recommended_action"}]
    df[clean_columns].to_csv(os.path.join(PROCESSED_DIR, "lokerlens_dataset_clean.csv"), index=False)
    df.to_csv(os.path.join(PROCESSED_DIR, "lokerlens_dataset_labeled.csv"), index=False)
    _red_flag_summary(df).to_csv(os.path.join(PROCESSED_DIR, "red_flag_summary.csv"), index=False)
    _write_data_dictionary(os.path.join(REPORTS_DIR, "data_dictionary.md"))
    logging.info("Saved %s labeled rows", len(df))

def _label_record(row, item_id):
    description = clean_text(row.get("raw_description", ""))
    requirements = clean_text(row.get("raw_requirements", ""))
    benefits = clean_text(row.get("raw_benefits", ""))
    text = clean_text(row.get("job_text", "")) or " ".join([description, requirements, benefits])
    salary = clean_text(row.get("raw_salary", ""))
    combined_text = " ".join([text, description, requirements, benefits, salary])
    compensation_status, compensation_text = detect_compensation(" ".join([combined_text, salary]))
    working_hours_status, working_hours_text = detect_working_hours(combined_text)
    duration_status, duration_text = detect_duration(combined_text)
    sensitive_status, sensitive_terms = detect_sensitive_data(combined_text)
    payment_status, payment_terms = detect_payment_request(combined_text)
    promise_status, promise_terms = detect_unrealistic_promise(combined_text)
    output = {
        "id": item_id,
        "source_name": clean_text(row.get("source_name", "")),
        "source_platform": normalize_platform(row.get("source_platform", "")),
        "source_url": clean_text(row.get("source_url", "")),
        "collected_at": clean_text(row.get("collected_at", "")) or datetime.utcnow().isoformat(timespec="seconds"),
        "job_title": clean_text(row.get("job_title", "")),
        "company_name": clean_text(row.get("company_name", "")),
        "job_type": normalize_job_type(row.get("job_type", "") or row.get("raw_employment_type", "")),
        "job_text": _sanitize_text(text),
        "job_description": _fallback_extract(description, combined_text, r"\b(job description|your role|responsibilities|what you will do|the role).{0,600}"),
        "requirements": requirements or _fallback_extract("", combined_text, r"\b(requirements|qualifications|your profile|what you need).{0,500}"),
        "benefits": benefits or _fallback_extract("", combined_text, r"\b(benefits|perks|what we offer|bonus).{0,500}"),
        "compensation_status": compensation_status,
        "compensation_text": compensation_text or salary,
        "working_hours_status": working_hours_status,
        "working_hours_text": working_hours_text,
        "work_arrangement": detect_work_arrangement(combined_text),
        "location": clean_text(row.get("location", "")),
        "duration_status": duration_status,
        "duration_text": duration_text,
        "contact_type": detect_contact_type(combined_text),
        "asks_sensitive_data": sensitive_status,
        "sensitive_data_terms": sensitive_terms,
        "asks_payment": payment_status,
        "payment_terms": payment_terms,
        "unrealistic_promise": promise_status,
        "unrealistic_promise_terms": promise_terms,
        "workload_status": detect_workload(combined_text),
        "notes": clean_text(row.get("notes", "")),
    }
    output["company_clarity"] = detect_company_clarity(output)
    output["missing_fields"] = detect_missing_fields(output)
    output["red_flag_categories"] = detect_red_flags(output)
    output["red_flag_count"] = len(_split_semicolon(output["red_flag_categories"]))
    output["trust_score"] = calculate_trust_score(output)
    output["risk_level"] = assign_risk_level(output["trust_score"])
    output["recommended_action"] = assign_recommended_action(output["risk_level"])
    return output

def _red_flag_summary(df):
    counts = {}
    for value in df["red_flag_categories"].fillna(""):
        for item in _split_semicolon(value):
            counts[item] = counts.get(item, 0) + 1
    return pd.DataFrame([{"red_flag_category": key, "count": value} for key, value in sorted(counts.items())])

def _write_data_dictionary(path):
    examples = {
        "source_name": "arbeitnow",
        "source_platform": "job_site",
        "trust_score": "84",
        "risk_level": "Cukup Aman, Tapi Perlu Dicek",
        "red_flag_categories": "compensation_missing;working_hours_missing",
    }
    with open(path, "w", encoding="utf-8") as file:
        file.write("# Data Dictionary\n\n")
        file.write("| Column | Type | Explanation | Example |\n")
        file.write("|---|---|---|---|\n")
        for column in FINAL_COLUMNS:
            file.write(f"| `{column}` | {_column_type(column)} | {_column_description(column)} | {examples.get(column, '')} |\n")

def _column_type(column):
    if column in {"id", "red_flag_count", "trust_score"}:
        return "integer"
    return "string"

def _column_description(column):
    descriptions = {
        "id": "Nomor unik baris data.",
        "source_name": "Nama sumber public API atau public page.",
        "source_platform": "Kategori platform sumber lowongan.",
        "source_url": "URL publik sumber lowongan.",
        "missing_fields": "Informasi penting yang tidak disebutkan, dipisahkan semicolon.",
        "red_flag_categories": "Kategori indikasi risiko berbasis rule-based.",
        "trust_score": "Skor 0-100 untuk transparansi dan indikasi risiko.",
        "risk_level": "Kategori risiko berdasarkan trust_score.",
        "recommended_action": "Rekomendasi awal untuk pelamar.",
    }
    return descriptions.get(column, column.replace("_", " ").capitalize())

def _extract_evidence(text, pattern):
    match = re.search(pattern, text, flags=re.I)
    return clean_text(match.group(0)) if match else ""

def _fallback_extract(value, text, pattern):
    return clean_text(value) or _extract_evidence(text, pattern)

def _sanitize_text(text):
    value = clean_text(text)
    value = re.sub(r"[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com", "personal_email", value, flags=re.I)
    value = re.sub(r"\b(\+?62|0)8[0-9\s.-]{7,}\b", "whatsapp_personal", value)
    value = re.sub(r"\b\d{8,16}\b", "sensitive_number_redacted", value)
    return value

def _has_pattern(text, pattern):
    return bool(re.search(pattern, clean_text(text), flags=re.I))

def _split_semicolon(value):
    return [item.strip() for item in clean_text(value).split(";") if item.strip()]

def main():
    df = build_labeled_dataset()
    save_outputs(df)

if __name__ == "__main__":
    main()
