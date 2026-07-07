import json
import logging
import os
import random
import re
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
SOURCE_URLS_PATH = os.path.join(RAW_DIR, "source_urls.txt")
SCRAPED_PATH = os.path.join(RAW_DIR, "scraped_job_posts.csv")
ERROR_PATH = os.path.join(RAW_DIR, "scraping_errors.csv")
LOG_PATH = os.path.join(RAW_DIR, "raw_collection_log.csv")

MAX_RECORDS = 300
MIN_TARGET_RECORDS = 200
REQUEST_TIMEOUT = 20
USER_AGENT = "LokerLensDataModule/1.1 (+academic public job data collection)"

RAW_COLUMNS = [
    "source_name",
    "source_platform",
    "source_url",
    "collected_at",
    "job_title",
    "company_name",
    "location",
    "job_type",
    "job_text",
    "raw_description",
    "raw_requirements",
    "raw_benefits",
    "raw_salary",
    "raw_employment_type",
    "notes",
]

BLOCKED_PHRASES = [
    "access denied",
    "are you a human",
    "captcha",
    "cf-chl",
    "cloudflare",
    "forbidden",
    "login to continue",
    "please log in",
    "please sign in",
    "security check",
    "verify you are human",
]

NAVIGATION_WORDS = {
    "apply",
    "apply now",
    "company",
    "detail",
    "details",
    "jobs",
    "learn more",
    "login",
    "read more",
    "register",
    "save",
    "search",
    "sign in",
    "view",
    "view job",
}

GENERIC_TITLE_EXACT = {
    "all jobs",
    "company",
    "contract",
    "daftar loker",
    "engineering",
    "freelance",
    "fresh graduate",
    "full time",
    "full-time",
    "internship",
    "job search",
    "jobs",
    "loker",
    "magang",
    "marketing",
    "marketing & communications",
    "melamar mudah",
    "part time",
    "part-time",
    "perusahaan",
    "refine your search",
    "remote",
    "type",
}

TITLE_NOISE_PATTERNS = [
    r"\bbergabung sekarang\b",
    r"\bdaftar loker\b",
    r"\bjob search\b",
    r"\bkurang dari\s+\d+\s+pelamar\b",
    r"\blowongan kerja (magang|freelance|paruh waktu|penuh waktu)\s+\w+\s+\d{4}\b",
    r"\bmelamar mudah\b",
    r"\brelated searches\b",
    r"\brefine your search\b",
    r"\bshow classifications\b",
    r"\btanggal posting\b",
    r"^\W+.*\bjobs\b",
]

COMPANY_NOISE_PATTERNS = [
    r"\bdaftar loker\b",
    r"\bjobstreet\b",
    r"\bloker\b",
    r"\bpelamar masih sedikit\b",
    r"\brefine your search\b",
    r"\btanggal posting\b",
]

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def ensure_directories():
    os.makedirs(RAW_DIR, exist_ok=True)

def clean_text(value):
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    if isinstance(value, (list, tuple, set)):
        value = " ".join(clean_text(item) for item in value)
    elif isinstance(value, dict):
        value = json.dumps(value, ensure_ascii=True)
    text = str(value)
    text = re.sub(r"<br\s*/?>", " ", text, flags=re.I)
    text = re.sub(r"</(p|li|div|h1|h2|h3)>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    replacements = {
        "&nbsp;": " ",
        "&#160;": " ",
        "&amp;": "&",
        "&quot;": '"',
        "&#39;": "'",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def infer_platform(url):
    domain = urlparse(str(url)).netloc.lower()
    if any(token in domain for token in ["arbeitnow", "themuse", "remotive", "remoteok"]):
        return "job_site"
    if "linkedin" in domain:
        return "linkedin"
    if "instagram" in domain:
        return "instagram"
    if "twitter" in domain or "x.com" in domain:
        return "twitter_x"
    if "telegram" in domain or "t.me" in domain:
        return "telegram"
    if any(token in domain for token in ["dealls", "indeed", "jobstreet", "job", "career", "karir", "prosple"]):
        return "job_site"
    return "company_website" if domain else "other"

def safe_get(url, headers=None):
    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
    }
    if headers:
        request_headers.update(headers)
    response = requests.get(url, headers=request_headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response

def collect_from_source_urls(urls):
    records = []
    errors = []
    logs = []

    for url in urls:
        source_name = source_name_from_url(url)
        try:
            if is_json_api_url(url):
                response = safe_get(url, headers={"Accept": "application/json,*/*;q=0.8"})
                payload = response.json()
                source_records = parse_json_api_url(url, payload)
            else:
                response = safe_get(url, headers={"Accept": "text/html,*/*;q=0.8"})
                source_records = parse_html_job_page(url, response.text)

            records.extend(source_records)
            logs.append(_log_row(source_name, len(source_records), "success", url))
            logging.info("%s collected %s records from %s", source_name, len(source_records), url)
        except Exception as exc:
            errors.append(_error_row(source_name, url, exc))
            logs.append(_log_row(source_name, 0, "failed", f"{url}: {exc}"))
            logging.warning("%s failed: %s", url, exc)

        time.sleep(random.uniform(0.4, 1.0) if is_json_api_url(url) else random.uniform(1.5, 4.0))

    return records, errors, logs

def parse_json_api_url(url, payload):
    source_name = source_name_from_url(url)
    parsers = {
        "arbeitnow": parse_arbeitnow_api,
        "remotive": parse_remotive_api,
        "themuse": parse_themuse_api,
        "remoteok": parse_remoteok_api,
    }
    parser = parsers.get(source_name)
    if not parser:
        raise ValueError(f"Unsupported JSON API source: {url}")
    return parser(payload, url)

def parse_arbeitnow_api(payload, api_url):
    items = payload.get("data", []) if isinstance(payload, dict) else []
    records = []
    for item in items:
        description = clean_text(item.get("description", ""))
        job_types = _join_list(item.get("job_types", []))
        title = clean_text(item.get("title", ""))
        company = clean_text(item.get("company_name", ""))
        records.append(normalize_raw_record({
            "source_name": "arbeitnow",
            "source_platform": "job_site",
            "source_url": item.get("url") or api_url,
            "collected_at": _timestamp_from_unix(item.get("created_at")),
            "job_title": title,
            "company_name": company,
            "location": item.get("location", ""),
            "job_type": _infer_job_type(" ".join([job_types, title, description])),
            "job_text": " ".join([title, company, description]),
            "raw_description": description,
            "raw_requirements": _extract_section(description, ["requirements", "your profile", "profile", "qualifications"]),
            "raw_benefits": _extract_section(description, ["benefits", "perks", "what we offer"]),
            "raw_salary": "",
            "raw_employment_type": job_types,
            "notes": f"public_api_arbeitnow; endpoint={api_url}",
        }))
    return records

def parse_remotive_api(payload, api_url):
    items = payload.get("jobs", []) if isinstance(payload, dict) else []
    records = []
    for item in items:
        description = clean_text(item.get("description", ""))
        title = clean_text(item.get("title", ""))
        company = clean_text(item.get("company_name", ""))
        employment_type = clean_text(item.get("job_type", ""))
        records.append(normalize_raw_record({
            "source_name": "remotive",
            "source_platform": "job_site",
            "source_url": item.get("url") or api_url,
            "collected_at": item.get("publication_date", ""),
            "job_title": title,
            "company_name": company,
            "location": item.get("candidate_required_location", ""),
            "job_type": _infer_job_type(" ".join([employment_type, title, description])),
            "job_text": " ".join([title, company, description]),
            "raw_description": description,
            "raw_requirements": _extract_section(description, ["requirements", "what you need", "qualifications"]),
            "raw_benefits": _extract_section(description, ["benefits", "perks", "what we offer"]),
            "raw_salary": item.get("salary", ""),
            "raw_employment_type": employment_type,
            "notes": f"public_api_remotive; endpoint={api_url}; attribution=remotive",
        }))
    return records

def parse_themuse_api(payload, api_url):
    items = payload.get("results", []) if isinstance(payload, dict) else []
    records = []
    for item in items:
        description = clean_text(item.get("contents", ""))
        company = item.get("company", {}) or {}
        locations = item.get("locations", []) or []
        levels = item.get("levels", []) or []
        categories = item.get("categories", []) or []
        title = clean_text(item.get("name", ""))
        company_name = clean_text(company.get("name", ""))
        level_text = _join_list([level.get("name", "") for level in levels])
        category_text = _join_list([category.get("name", "") for category in categories])
        employment_type = clean_text(item.get("type", ""))
        records.append(normalize_raw_record({
            "source_name": "themuse",
            "source_platform": "job_site",
            "source_url": (item.get("refs", {}) or {}).get("landing_page", "") or api_url,
            "collected_at": item.get("publication_date", ""),
            "job_title": title,
            "company_name": company_name,
            "location": _join_list([location.get("name", "") for location in locations]),
            "job_type": _infer_job_type(" ".join([employment_type, level_text, category_text, title, description])),
            "job_text": " ".join([title, company_name, description]),
            "raw_description": description,
            "raw_requirements": _extract_section(description, ["qualifications", "requirements", "minimum qualifications"]),
            "raw_benefits": _extract_section(description, ["benefits", "bonus", "what we offer"]),
            "raw_salary": "",
            "raw_employment_type": employment_type or level_text,
            "notes": f"public_api_themuse; endpoint={api_url}",
        }))
    return records

def parse_remoteok_api(payload, api_url):
    if not isinstance(payload, list):
        raise ValueError("Remote OK payload is not a list")

    records = []
    for item in payload:
        if not isinstance(item, dict) or not item.get("position"):
            continue
        description = clean_text(item.get("description", ""))
        title = clean_text(item.get("position", ""))
        company = clean_text(item.get("company", ""))
        tags = _join_list(item.get("tags", []))
        salary = _format_remoteok_salary(item)
        employment_type = clean_text(item.get("type", "")) or tags
        source_url = item.get("url") or item.get("apply_url") or api_url
        records.append(normalize_raw_record({
            "source_name": "remoteok",
            "source_platform": "job_site",
            "source_url": source_url,
            "collected_at": item.get("date", "") or item.get("epoch", ""),
            "job_title": title,
            "company_name": company,
            "location": item.get("location", "") or "Remote",
            "job_type": _infer_job_type(" ".join([employment_type, title, description])),
            "job_text": " ".join([title, company, tags, description]),
            "raw_description": description,
            "raw_requirements": _extract_section(description, ["requirements", "qualifications", "what you need"]),
            "raw_benefits": _extract_section(description, ["benefits", "perks", "what we offer"]),
            "raw_salary": salary,
            "raw_employment_type": employment_type,
            "notes": f"public_api_remoteok; endpoint={api_url}",
        }))
    return records

def parse_html_job_page(url, html):
    if BeautifulSoup is None:
        raise RuntimeError("BeautifulSoup is required for HTML job page parsing")

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.decompose()

    page_text = clean_text(soup.get_text(" ", strip=True))
    if _looks_blocked_page(page_text):
        raise ValueError("HTML page appears blocked, login-gated, or captcha-protected")

    source_name = source_name_from_url(url)
    records = _extract_json_ld_jobs(soup, url, source_name)
    records.extend(_extract_anchor_jobs(soup, url, source_name))

    normalized = []
    seen = set()
    for record in records:
        candidate = normalize_raw_record(record)
        key = (
            candidate["source_url"].lower(),
            candidate["job_title"].lower(),
            candidate["company_name"].lower(),
        )
        if candidate["job_title"] and key not in seen:
            normalized.append(candidate)
            seen.add(key)

    if not normalized:
        raise ValueError("HTML job cards could not be parsed from this page")

    return normalized[:80]

def normalize_raw_record(record):
    normalized = {column: clean_text(record.get(column, "")) for column in RAW_COLUMNS}
    normalized["source_platform"] = normalized["source_platform"] or infer_platform(normalized["source_url"])
    normalized["collected_at"] = normalized.get("collected_at") or datetime.utcnow().isoformat(timespec="seconds")
    normalized["job_text"] = _sanitize_sensitive_text(normalized["job_text"])
    for column in ["raw_description", "raw_requirements", "raw_benefits"]:
        normalized[column] = _sanitize_sensitive_text(normalized[column])
    if not normalized["job_text"]:
        normalized["job_text"] = " ".join([
            normalized["job_title"],
            normalized["company_name"],
            normalized["location"],
            normalized["raw_description"],
        ]).strip()
    return normalized

def deduplicate_jobs(df):
    if df.empty:
        return df
    frame = df.copy()
    frame["_dedupe_key"] = (
        frame["source_url"].fillna("").str.lower().str.strip()
        + "|"
        + frame["job_title"].fillna("").str.lower().str.strip()
        + "|"
        + frame["company_name"].fillna("").str.lower().str.strip()
        + "|"
        + frame["job_text"].fillna("").str.lower().str[:220]
    )
    frame = frame.drop_duplicates("_dedupe_key").drop(columns=["_dedupe_key"])
    if len(frame) <= MAX_RECORDS:
        return frame.reset_index(drop=True)

    selected_indices = []
    source_names = [source for source in frame["source_name"].fillna("unknown").unique() if clean_text(source)]
    per_source_quota = max(1, MAX_RECORDS // max(1, len(source_names)))
    for source_name in source_names:
        source_rows = frame[frame["source_name"].fillna("unknown") == source_name].head(per_source_quota)
        selected_indices.extend(source_rows.index.tolist())

    selected = frame.loc[selected_indices].drop_duplicates()
    remaining_slots = MAX_RECORDS - len(selected)
    if remaining_slots > 0:
        remaining = frame.drop(index=selected_indices, errors="ignore").head(remaining_slots)
        selected = pd.concat([selected, remaining], ignore_index=False)

    return selected.head(MAX_RECORDS).reset_index(drop=True)

def save_dataframe(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def save_errors(errors, path):
    columns = ["source_name", "source_url", "error_type", "error_message", "collected_at"]
    pd.DataFrame(errors, columns=columns).to_csv(path, index=False)

def save_collection_log(logs, path):
    columns = ["source_name", "records_collected", "status", "notes", "collected_at"]
    pd.DataFrame(logs, columns=columns).to_csv(path, index=False)

def main():
    setup_logging()
    ensure_directories()

    urls = load_source_urls(SOURCE_URLS_PATH)
    if not urls:
        raise FileNotFoundError(f"No active source URLs found in {SOURCE_URLS_PATH}")

    records, errors, logs = collect_from_source_urls(urls)
    df = deduplicate_jobs(pd.DataFrame(records, columns=RAW_COLUMNS))

    if len(df) < MIN_TARGET_RECORDS:
        warning = "Collected less than 200 records. No synthetic data was generated."
        logging.warning(warning)
        logs.append(_log_row("collection_warning", len(df), "warning", warning))

    save_dataframe(df, SCRAPED_PATH)
    save_errors(errors, ERROR_PATH)
    save_collection_log(logs, LOG_PATH)
    logging.info("Final raw dataset saved with %s records", len(df))

def load_source_urls(path):
    if not os.path.exists(path):
        return []
    urls = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            value = line.strip()
            if value and not value.startswith("#"):
                urls.append(value)
    return urls

def is_json_api_url(url):
    parsed = urlparse(url)
    path = parsed.path.lower()
    domain = parsed.netloc.lower()
    return (
        "/api/" in path
        or path.endswith("/api")
        or "remoteok.com" in domain and path == "/api"
        or "api." in domain
    )

def source_name_from_url(url):
    domain = urlparse(str(url)).netloc.lower()
    if "arbeitnow" in domain:
        return "arbeitnow"
    if "remotive" in domain:
        return "remotive"
    if "themuse" in domain:
        return "themuse"
    if "remoteok" in domain:
        return "remoteok"
    if "dealls" in domain:
        return "dealls"
    if "jobstreet" in domain:
        return "jobstreet"
    if "indeed" in domain:
        return "indeed"
    if "prosple" in domain:
        return "prosple"
    if "linkedin" in domain:
        return "linkedin"
    return domain.replace("www.", "").split(".")[0] or "source_urls"

def _extract_json_ld_jobs(soup, page_url, source_name):
    records = []
    for script in soup.find_all("script", attrs={"type": re.compile("ld\\+json", re.I)}):
        raw = script.string or script.get_text()
        if not raw:
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for item in _iter_json_ld_nodes(payload):
            if clean_text(item.get("@type", "")).lower() != "jobposting":
                continue
            title = clean_text(item.get("title", ""))
            description = clean_text(item.get("description", ""))
            company = item.get("hiringOrganization", {}) or {}
            location = _json_ld_location(item.get("jobLocation", ""))
            salary = clean_text(item.get("baseSalary", ""))
            employment_type = _join_list(item.get("employmentType", ""))
            records.append({
                "source_name": source_name,
                "source_platform": infer_platform(page_url),
                "source_url": item.get("url") or page_url,
                "collected_at": item.get("datePosted", "") or datetime.utcnow().isoformat(timespec="seconds"),
                "job_title": title,
                "company_name": company.get("name", "") if isinstance(company, dict) else "",
                "location": location,
                "job_type": _infer_job_type(" ".join([employment_type, title, description])),
                "job_text": " ".join([title, description]),
                "raw_description": description,
                "raw_requirements": _extract_section(description, ["requirements", "qualifications", "persyaratan"]),
                "raw_benefits": _extract_section(description, ["benefits", "perks", "benefit", "tunjangan"]),
                "raw_salary": salary,
                "raw_employment_type": employment_type,
                "notes": "html_json_ld_jobposting",
            })
    return records

def _extract_anchor_jobs(soup, page_url, source_name):
    records = []
    for anchor in soup.find_all("a", href=True):
        href = clean_text(anchor.get("href", ""))
        detail_url = urljoin(page_url, href)
        if not _is_source_detail_link(source_name, detail_url):
            continue
        title = _candidate_title(anchor)
        if not _is_likely_job_anchor(title, href):
            continue

        card = _nearest_job_container(anchor)
        card_text = clean_text(card.get_text(" ", strip=True)) if card else title
        if _is_noise_card_text(card_text, source_name):
            continue
        card_text = _slice_card_text_around_title(card_text, title)
        if len(card_text) < 20:
            continue

        company = _extract_company_from_card(card, title)
        source_company = _extract_company_from_card_text(source_name, card_text, title)
        if source_company:
            company = source_company
        company_from_url = _extract_company_from_detail_url(detail_url, source_name)
        if company_from_url or _is_noise_company(company):
            company = company_from_url
        location = _extract_location_from_card_text(source_name, card_text) or _extract_location_from_card(card_text)
        salary = _extract_salary_from_text(card_text)
        employment_type = _extract_employment_type_from_text(card_text)
        job_text = clean_text(" ".join([title, company, location, card_text]))
        records.append({
            "source_name": source_name,
            "source_platform": infer_platform(page_url),
            "source_url": detail_url,
            "collected_at": datetime.utcnow().isoformat(timespec="seconds"),
            "job_title": title,
            "company_name": company,
            "location": location,
            "job_type": _infer_job_type(" ".join([employment_type, title, card_text])),
            "job_text": job_text,
            "raw_description": card_text[:2500],
            "raw_requirements": _extract_section(card_text, ["requirements", "qualifications", "persyaratan", "kualifikasi"]),
            "raw_benefits": _extract_section(card_text, ["benefits", "perks", "benefit", "tunjangan"]),
            "raw_salary": salary,
            "raw_employment_type": employment_type,
            "notes": "html_anchor_job_card",
        })
    return records

def _is_source_detail_link(source_name, detail_url):
    parsed = urlparse(detail_url)
    path = parsed.path.lower()
    if source_name == "dealls":
        return path.startswith("/loker/") and "~" in path
    if source_name == "jobstreet":
        return path.startswith("/job/")
    if source_name == "linkedin":
        return "/jobs/view/" in path
    return True

def _candidate_title(anchor):
    text = clean_text(anchor.get_text(" ", strip=True))
    if text.lower() in NAVIGATION_WORDS or len(text) < 4:
        return ""
    heading = anchor.find(["h1", "h2", "h3", "h4"])
    if heading:
        heading_text = clean_text(heading.get_text(" ", strip=True))
        if heading_text and heading_text.lower() not in NAVIGATION_WORDS:
            return heading_text
    return text[:150]

def _is_likely_job_anchor(title, href):
    if not title:
        return False
    lowered_title = title.lower()
    lowered_href = href.lower()
    if lowered_title in NAVIGATION_WORDS or lowered_title in GENERIC_TITLE_EXACT or _is_noise_title(title):
        return False
    if len(title) > 150 or len(title.split()) > 18:
        return False
    href_signal = any(token in lowered_href for token in [
        "/job",
        "/jobs",
        "/loker",
        "/lowongan",
        "/karir",
        "/careers",
        "viewjob",
        "jk=",
        "graduate-jobs",
        "internship-jobs",
    ])
    title_signal = any(token in lowered_title for token in [
        "analyst",
        "associate",
        "consultant",
        "developer",
        "engineer",
        "freelance",
        "graduate",
        "intern",
        "internship",
        "junior",
        "magang",
        "manager",
        "marketing",
        "part time",
        "part-time",
        "staff",
        "specialist",
        "trainee",
    ])
    return href_signal or title_signal

def _is_noise_title(title):
    lowered = clean_text(title).lower()
    return any(re.search(pattern, lowered, flags=re.I) for pattern in TITLE_NOISE_PATTERNS)

def _is_noise_card_text(text, source_name):
    lowered = clean_text(text).lower()
    if source_name == "jobstreet":
        return any(token in lowered for token in [
            "related searches",
            "refine your search",
            "show classifications refinements",
            "show salary range refinements",
            "show work type refinements",
        ])
    return False

def _slice_card_text_around_title(text, title):
    cleaned = clean_text(text)
    index = cleaned.lower().find(clean_text(title).lower())
    if index < 0:
        return cleaned[:1200]
    return clean_text(cleaned[index:index + 1200])

def _extract_company_from_card_text(source_name, card_text, title):
    if source_name == "jobstreet":
        pattern = re.escape(clean_text(title)) + r"\s+at\s+(.+?)\s+This is a\b"
        match = re.search(pattern, clean_text(card_text), flags=re.I)
        if match:
            return clean_text(match.group(1))[:120]
    return ""

def _extract_location_from_card_text(source_name, card_text):
    text = clean_text(card_text)
    if source_name == "jobstreet":
        match = re.search(r"\bThis is a\s+.+?\s+job\s+(.+?)(?:\s+Rp|\s+subClassification|\s+classification|\s+\d+d ago|$)", text, flags=re.I)
        if match:
            return clean_text(match.group(1))[:120]
    return ""

def _nearest_job_container(anchor):
    node = anchor
    best = anchor.parent
    for _ in range(6):
        if not node or not getattr(node, "parent", None):
            break
        node = node.parent
        text = clean_text(node.get_text(" ", strip=True))
        if 40 <= len(text) <= 2500:
            best = node
            class_text = " ".join(node.get("class", [])) if hasattr(node, "get") else ""
            attr_text = " ".join([class_text, str(node.get("data-testid", "")), str(node.get("data-automation", ""))]).lower()
            if any(token in attr_text for token in ["job", "card", "posting", "vacancy", "loker"]):
                return node
    return best

def _extract_company_from_card(card, title):
    if not card:
        return ""
    selectors = [
        "[class*=company]",
        "[class*=employer]",
        "[data-testid*=company]",
        "[data-automation*=company]",
        "[aria-label*=company]",
    ]
    for selector in selectors:
        found = card.select_one(selector)
        if found:
            text = clean_text(found.get_text(" ", strip=True))
            if _is_plausible_company(text, title):
                return text[:120]

    lines = [clean_text(line) for line in card.get_text("\n", strip=True).splitlines()]
    lines = [line for line in lines if line and line.lower() not in NAVIGATION_WORDS]
    for line in lines:
        if line.lower() == title.lower():
            continue
        if _is_plausible_company(line, title):
            return line[:120]
    return ""

def _is_plausible_company(text, title):
    lowered = text.lower()
    if not text or text.lower() == title.lower():
        return False
    if len(text) > 120 or len(text.split()) > 12:
        return False
    if any(re.search(pattern, lowered, flags=re.I) for pattern in COMPANY_NOISE_PATTERNS):
        return False
    if any(token in lowered for token in ["apply", "login", "salary", "remote", "full-time", "part-time"]):
        return False
    return True

def _is_noise_company(text):
    if not clean_text(text):
        return True
    lowered = clean_text(text).lower()
    return any(re.search(pattern, lowered, flags=re.I) for pattern in COMPANY_NOISE_PATTERNS)

def _extract_company_from_detail_url(detail_url, source_name):
    if source_name != "dealls":
        return ""
    path = urlparse(detail_url).path
    if "~" not in path:
        return ""
    slug = path.rsplit("~", 1)[-1].strip("/")
    slug = re.sub(r"[^A-Za-z0-9-]+", "", slug)
    if not slug:
        return ""
    return clean_text(slug.replace("-", " ").title())

def _extract_location_from_card(text):
    patterns = [
        r"\b(?:Jakarta|Bandung|Surabaya|Yogyakarta|Jogja|Bali|Denpasar|Tangerang|Bekasi|Depok|Bogor|Semarang|Medan|Makassar|Indonesia|Remote|Hybrid|On-site|Onsite|WFH|WFO)[A-Za-z,\s-]{0,60}",
        r"\b(?:New York|San Francisco|London|Berlin|Singapore|Australia|United States|Europe|Worldwide|EMEA|APAC)[A-Za-z,\s-]{0,60}",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return clean_text(match.group(0))[:120]
    return ""

def _extract_salary_from_text(text):
    pattern = r"((?:Rp|IDR|\$|USD|EUR|SGD)\s?[0-9][0-9.,kKmM\s-]{2,40}(?:/bulan|/month|per month|monthly|annually|per year)?)"
    match = re.search(pattern, text, flags=re.I)
    return clean_text(match.group(1)) if match else ""

def _extract_employment_type_from_text(text):
    matches = re.findall(
        r"\b(full[- ]time|part[- ]time|internship|intern|magang|freelance|contract|temporary|fresh graduate|entry level|graduate)\b",
        text,
        flags=re.I,
    )
    return _join_list(dict.fromkeys(matches))

def _infer_job_type(text):
    lowered = clean_text(text).lower()
    if re.search(r"\b(internship|intern|magang)\b", lowered):
        return "internship"
    if re.search(r"\b(freelance|contractor)\b", lowered):
        return "freelance"
    if re.search(r"\b(part[-_ ]time|parttime)\b", lowered):
        return "part_time"
    if re.search(r"\b(entry level|fresh graduate|graduate|junior|associate|trainee)\b", lowered):
        return "entry_level"
    return "unknown"

def _html_to_text(html):
    if BeautifulSoup:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "svg"]):
            tag.decompose()
        return clean_text(soup.get_text(" ", strip=True))
    return clean_text(html)

def _looks_blocked_page(text):
    lowered = clean_text(text).lower()
    if any(phrase in lowered for phrase in BLOCKED_PHRASES):
        return True
    return len(lowered) < 300 and any(token in lowered for token in ["login", "sign in", "javascript"])

def _iter_json_ld_nodes(payload):
    if isinstance(payload, dict):
        if "@graph" in payload:
            for item in _iter_json_ld_nodes(payload["@graph"]):
                yield item
        else:
            yield payload
    elif isinstance(payload, list):
        for item in payload:
            yield from _iter_json_ld_nodes(item)

def _json_ld_location(value):
    if isinstance(value, list):
        return _join_list([_json_ld_location(item) for item in value])
    if not isinstance(value, dict):
        return clean_text(value)
    address = value.get("address", {}) or {}
    if isinstance(address, dict):
        return _join_list([
            address.get("addressLocality", ""),
            address.get("addressRegion", ""),
            address.get("addressCountry", ""),
        ])
    return clean_text(address)

def _extract_section(text, headings):
    lowered = clean_text(text).lower()
    for heading in headings:
        index = lowered.find(heading.lower())
        if index >= 0:
            return clean_text(text[index:index + 800])
    return ""

def _sanitize_sensitive_text(text):
    value = clean_text(text)
    value = re.sub(r"[A-Za-z0-9._%+-]+@(gmail|yahoo|outlook|hotmail)\.com", "personal_email", value, flags=re.I)
    value = re.sub(r"\b(\+?62|0)8[0-9\s.-]{7,}\b", "whatsapp_personal", value)
    value = re.sub(r"\b\d{8,16}\b", "sensitive_number_redacted", value)
    return value

def _timestamp_from_unix(value):
    try:
        return datetime.utcfromtimestamp(int(value)).isoformat(timespec="seconds")
    except Exception:
        return datetime.utcnow().isoformat(timespec="seconds")

def _format_remoteok_salary(item):
    salary = clean_text(item.get("salary", ""))
    if salary:
        return salary
    salary_min = clean_text(item.get("salary_min", ""))
    salary_max = clean_text(item.get("salary_max", ""))
    if salary_min or salary_max:
        return "-".join(value for value in [salary_min, salary_max] if value)
    return ""

def _join_list(values):
    if isinstance(values, str):
        return clean_text(values)
    if not isinstance(values, (list, tuple, set)):
        return clean_text(values)
    return "; ".join(clean_text(value) for value in values if clean_text(value))

def _error_row(source_name, source_url, exc):
    return {
        "source_name": source_name,
        "source_url": source_url,
        "error_type": type(exc).__name__,
        "error_message": str(exc),
        "collected_at": datetime.utcnow().isoformat(timespec="seconds"),
    }

def _log_row(source_name, count, status, notes):
    return {
        "source_name": source_name,
        "records_collected": count,
        "status": status,
        "notes": notes,
        "collected_at": datetime.utcnow().isoformat(timespec="seconds"),
    }

if __name__ == "__main__":
    main()
