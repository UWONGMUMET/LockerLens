from __future__ import annotations

import re
from dataclasses import dataclass

@dataclass(frozen=True)
class RiskRule:
    category: str
    severity: str
    deduction: int
    patterns: tuple[str, ...]
    explanation: str

@dataclass(frozen=True)
class HighlightRule:
    category: str
    severity: str
    patterns: tuple[str, ...]
    explanation: str

RISK_RULES: tuple[RiskRule, ...] = (
    RiskRule(
        category="Meminta biaya pendaftaran atau deposit",
        severity="high",
        deduction=30,
        patterns=(
            r"\b(biaya|uang|deposit|admin|administrasi|registrasi|pendaftaran)\b.{0,45}\b(daftar|join|training|seragam|materai|jaminan|transfer|bayar|membayar)\b",
            r"\b(bayar|transfer)\b.{0,35}\b(sebelum|dulu|awal|pendaftaran|registrasi|interview)\b",
            r"\b(deposit|biaya pendaftaran|biaya admin|biaya administrasi)\b",
        ),
        explanation="Lowongan yang meminta pembayaran di awal perlu diverifikasi karena proses rekrutmen normal biasanya tidak membebankan biaya kepada pelamar.",
    ),
    RiskRule(
        category="Meminta data pribadi sensitif terlalu awal",
        severity="high",
        deduction=25,
        patterns=(
            r"\b(ktp|kartu tanda penduduk|foto ktp|selfie ktp|kartu keluarga|kk|otp|password|kata sandi|pin|rekening|nomor rekening)\b",
            r"\b(data pribadi lengkap|dokumen identitas)\b.{0,40}\b(sebelum|awal|pendaftaran|interview|seleksi)\b",
        ),
        explanation="Data seperti KTP, rekening, OTP, atau password sebaiknya tidak diminta pada tahap awal tanpa proses resmi yang jelas.",
    ),
    RiskRule(
        category="Identitas perusahaan tidak jelas",
        severity="high",
        deduction=20,
        patterns=(
            r"\b(company confidential|perusahaan rahasia|perusahaan berkembang|brand besar|kantor cabang baru)\b",
            r"\b(nama perusahaan|identitas perusahaan)\b.{0,35}\b(dirahasiakan|menyusul|tidak disebutkan)\b",
        ),
        explanation="Identitas perusahaan yang kabur membuat pelamar sulit memverifikasi reputasi dan kanal resmi rekrutmen.",
    ),
    RiskRule(
        category="Janji penghasilan tidak realistis",
        severity="high",
        deduction=20,
        patterns=(
            r"\b(penghasilan|income|gaji|komisi|cuan)\b.{0,45}\b(jutaan|puluhan juta|tidak terbatas|unlimited|fantastis)\b",
            r"\b(kerja|modal)\b.{0,35}\b(mudah|santai|tanpa pengalaman)\b.{0,45}\b(jutaan|puluhan juta|income besar)\b",
        ),
        explanation="Klaim penghasilan yang terlalu tinggi atau tidak disertai struktur kompensasi jelas perlu diverifikasi lebih dulu.",
    ),
    RiskRule(
        category="Unpaid dengan beban kerja berat",
        severity="medium",
        deduction=15,
        patterns=(
            r"\b(unpaid|tidak dibayar|tanpa gaji|sukarela)\b.{0,80}\b(full.?time|setiap hari|target|deadline|berat|banyak|intensif)\b",
            r"\b(full.?time|setiap hari|target|deadline|berat|banyak|intensif)\b.{0,80}\b(unpaid|tidak dibayar|tanpa gaji|sukarela)\b",
        ),
        explanation="Program tanpa kompensasi dengan workload besar perlu ditanyakan batas tugas, jam kerja, dan manfaat konkretnya.",
    ),
    RiskRule(
        category="Jobdesc terlalu luas atau ambigu",
        severity="medium",
        deduction=10,
        patterns=(
            r"\b(serabutan|all.?rounder|multitasking tinggi|mengerjakan semua|siap ditempatkan dimana saja)\b",
            r"\b(tugas lain|pekerjaan lain)\b.{0,45}\b(dibutuhkan|diperlukan|diminta)\b",
        ),
        explanation="Jobdesc yang terlalu luas bisa membuat ekspektasi kerja tidak jelas dan sulit dibatasi.",
    ),
    RiskRule(
        category="Jam fleksibel tanpa detail",
        severity="medium",
        deduction=10,
        patterns=(
            r"\b(jam|waktu)\b.{0,20}\b(fleksibel|flexible)\b(?!.*\b(per minggu|per hari|senin|shift|jam kerja|09\.00|10\.00|wib)\b)",
        ),
        explanation="Klaim jam fleksibel tetap perlu dilengkapi estimasi waktu, shift, atau batas workload.",
    ),
    RiskRule(
        category="Kontak rekrutmen kurang profesional",
        severity="medium",
        deduction=10,
        patterns=(
            r"\b(dm aja|dm saja|direct message|inbox|chat admin|wa saja|whatsapp only|chat personal|wa personal)\b",
            r"\b(email|kirim cv)\b.{0,30}\b(gmail\.com|yahoo\.com|hotmail\.com)\b",
        ),
        explanation="Kanal kontak pribadi bukan selalu berbahaya, tetapi sebaiknya diverifikasi dengan kanal resmi perusahaan.",
    ),
)

HIGHLIGHT_RULES: tuple[HighlightRule, ...] = (
    HighlightRule("Meminta biaya pendaftaran atau deposit", "high", (r"\bbiaya pendaftaran\b", r"\bdeposit\b", r"\bbiaya admin(?:istrasi)?\b"), "Pembayaran di awal perlu diverifikasi."),
    HighlightRule("Meminta data pribadi sensitif terlalu awal", "high", (r"\bktp\b", r"\brekening\b", r"\botp\b", r"\bpassword\b", r"\bkartu keluarga\b", r"\bkk\b"), "Data pribadi sensitif tidak aman diberikan terlalu awal."),
    HighlightRule("Janji penghasilan tidak realistis", "high", (r"\bpenghasilan tidak terbatas\b", r"\bunlimited income\b", r"\bpenghasilan jutaan\b", r"\bkerja mudah\b"), "Klaim penghasilan perlu bukti struktur kompensasi."),
    HighlightRule("Unpaid dengan beban kerja berat", "medium", (r"\bunpaid\b", r"\btidak dibayar\b", r"\btanpa gaji\b", r"\bfull.?time\b", r"\btarget\b"), "Workload dan kompensasi perlu dibatasi dengan jelas."),
    HighlightRule("Jobdesc terlalu luas atau ambigu", "medium", (r"\bserabutan\b", r"\ball.?rounder\b", r"\bmengerjakan semua\b", r"\bmultitasking tinggi\b"), "Jobdesc terlalu luas perlu diperjelas."),
    HighlightRule("Kontak rekrutmen kurang profesional", "medium", (r"\bwa saja\b", r"\bwhatsapp only\b", r"\bchat personal\b", r"\bdm aja\b"), "Kanal personal perlu dicek dengan kanal resmi."),
    HighlightRule("Benefit terlalu umum", "low", (r"\bsertifikat\b", r"\bpengalaman\b", r"\brelasi\b", r"\bnetworking\b"), "Benefit umum sebaiknya dilengkapi manfaat konkret."),
)

COMPENSATION_PATTERNS = (
    r"\b(gaji|salary|kompensasi|fee|honor|upah|bayaran|paid|dibayar|uang saku|insentif|range gaji)\b",
)
WORK_TIME_PATTERNS = (
    r"\b(jam kerja|working hours|shift|senin|selasa|rabu|kamis|jumat|sabtu|minggu|part.?time|full.?time|per minggu|per hari)\b",
)
COMPANY_PATTERNS = (
    r"\b(pt|cv|yayasan|universitas|kampus|studio|agency|corp|company|inc|ltd|llc|startup|perusahaan)\b",
    r"[A-Za-z0-9._%+-]+@(?!gmail\.com|yahoo\.com|hotmail\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
)
POSITION_PATTERNS = (
    r"\b(posisi|role|jabatan|dibutuhkan|mencari|open position|lowongan|internship|magang|freelance|part.?time|entry.?level)\b.{0,80}",
)
JOB_TYPE_PATTERNS = (
    r"\b(magang|internship|freelance|part.?time|entry.?level|full.?time|kontrak|project based)\b",
)
ROLE_DETAIL_PATTERNS = (
    r"\b(jobdesc|job description|deskripsi pekerjaan|tanggung jawab|responsibilities|kualifikasi|requirements|membuat|mengelola|menganalisis|menulis|desain|coding|melayani|support)\b",
)
DURATION_PATTERNS = (
    r"\b(durasi|periode|kontrak|mulai|start date|bulan|minggu|probation|masa kerja|selama)\b",
)
WORK_ARRANGEMENT_PATTERNS = (
    r"\b(wfo|wfh|remote|hybrid|onsite|on-site|work from office|work from home)\b",
)
SUPERVISION_PATTERNS = (
    r"\b(supervisor|mentor|manager|atasan|report to|lapor ke|pembimbing|pic|penanggung jawab)\b",
)
LOCATION_PATTERNS = (
    r"\b(lokasi|alamat|remote|hybrid|wfo|wfh|onsite|on-site|jakarta|bandung|surabaya|yogyakarta|semarang|medan|bali)\b",
)
BENEFIT_ONLY_PATTERNS = (
    r"\b(pengalaman|sertifikat|relasi|networking|portfolio|portofolio)\b",
)
CONTACT_PATTERNS = (
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    r"\b(wa|whatsapp|telegram|dm|direct message|email|kirim cv)\b.{0,55}",
)
CONTRACT_PATTERNS = (
    r"\b(kontrak|perjanjian|offer letter|surat penawaran|mou|agreement|nda)\b",
)
DOCUMENT_REQUIREMENT_PATTERNS = (
    r"\b(cv|resume|portofolio|portfolio|transkrip|ijazah|sertifikat|dokumen|berkas)\b",
)
DEADLINE_PATTERNS = (
    r"\b(deadline|batas apply|batas pendaftaran|ditutup|closing date|apply sebelum|maksimal)\b.{0,45}",
)
WORKLOAD_PATTERNS = (
    r"\b(full.?time|part.?time|target|deadline|setiap hari|per minggu|per hari|membuat|mengelola|reporting|shift)\b.{0,80}",
)
PERSONAL_DATA_PATTERNS = (
    r"\bktp\b",
    r"\brekening\b",
    r"\botp\b",
    r"\bpassword\b",
    r"\bkartu keluarga\b",
    r"\bkk\b",
    r"\bdeposit\b",
    r"\bbiaya pendaftaran\b",
    r"\bbiaya admin(?:istrasi)?\b",
)

MISSING_INFO_PENALTIES = {
    "Kompensasi": 10,
    "Jam kerja": 10,
    "Nama perusahaan": 15,
    "Jobdesc": 10,
    "Lokasi kerja": 5,
    "Work arrangement": 5,
    "Durasi program": 5,
    "Kontrak/perjanjian": 5,
    "Deadline apply": 3,
    "Supervisor/PIC": 5,
    "Kontak resmi": 10,
}

CRITICAL_MISSING_FIELDS = {
    "Kompensasi",
    "Nama perusahaan",
    "Jobdesc",
    "Jam kerja",
    "Kontak resmi",
}

SEVERE_RISK_CAP_CATEGORIES = {
    "Meminta biaya pendaftaran atau deposit",
    "Meminta data pribadi sensitif terlalu awal",
}

def analyze_job_text(
    job_text: str,
    job_type: str,
    source_platform: str,
    source_url: str | None = None,
    keywords: list[str] | None = None,
) -> dict:
    text = _squash(job_text)
    lowered = text.lower()
    cleaned_source_url = _clean_source_url(source_url)
    keywords_checked = _clean_keywords(keywords or [])
    score = 100
    red_flags: list[dict] = []
    score_breakdown: list[dict] = []

    for rule in RISK_RULES:
        evidence = _first_evidence(text, rule.patterns)
        if evidence:
            flag = _flag(rule.category, rule.severity, evidence, rule.explanation, rule.deduction)
            red_flags.append(flag)
            score_breakdown.append(_score_breakdown_item(flag))
            score -= rule.deduction

    missing_information = _missing_information(text)
    missing_breakdown = _missing_score_breakdown(missing_information)
    score -= sum(item["deduction"] for item in missing_breakdown)
    score_breakdown.extend(missing_breakdown)

    if _contains_any(lowered, BENEFIT_ONLY_PATTERNS) and not _contains_any(lowered, COMPENSATION_PATTERNS):
        flag = _flag(
            "Benefit terlalu umum",
            "low",
            _first_evidence(text, BENEFIT_ONLY_PATTERNS) or "Benefit disebutkan secara umum.",
            "Benefit seperti pengalaman atau sertifikat sebaiknya dilengkapi kompensasi, ruang belajar, atau learning plan yang jelas.",
            5,
        )
        red_flags.append(flag)
        score_breakdown.append(_score_breakdown_item(flag))
        score -= 5

    score = _apply_score_caps(score, missing_information, red_flags)
    score = max(0, min(100, score))
    risk_level = _risk_level(score)
    positive_signals = _positive_signals(text, source_platform)
    questions = _questions_to_ask(missing_information, red_flags, job_type)
    highlights = _highlighted_terms(text, missing_information)
    personal_warning = _personal_data_warning(text)
    checklist = _safe_apply_checklist(missing_information, red_flags, personal_warning)

    return {
        "trust_score": score,
        "risk_level": risk_level,
        "summary": _summary(score, risk_level, red_flags),
        "job_type": job_type,
        "source_platform": source_platform,
        "source_url": cleaned_source_url,
        "keywords_checked": keywords_checked,
        "job_summary": _job_summary(text, job_type, source_platform, red_flags),
        "highlighted_terms": highlights,
        "score_breakdown": score_breakdown,
        "red_flags": red_flags,
        "missing_information": missing_information,
        "missing_information_summary": _missing_information_summary(missing_information),
        "positive_signals": positive_signals,
        "questions_to_ask_recruiter": questions,
        "recommended_action": _recommended_action(score),
        "personal_data_warning": personal_warning,
        "safe_apply_checklist": checklist,
        "safety_note": "LokerLens membantu membaca indikasi risiko dari teks lowongan. Hasil ini bukan keputusan mutlak, jadi tetap verifikasi perusahaan, kanal rekrutmen, dan detail kerja sebelum mengirim data pribadi atau menerima tawaran.",
    }

def _flag(category: str, severity: str, evidence: str, explanation: str, deduction: int) -> dict:
    return {
        "category": category,
        "severity": severity,
        "evidence": evidence,
        "explanation": explanation,
        "deduction": deduction,
    }

def _score_breakdown_item(item: dict) -> dict:
    return {
        "category": item["category"],
        "evidence": item["evidence"],
        "deduction": item["deduction"],
        "explanation": item["explanation"],
    }

def _missing_score_breakdown(missing: list[dict]) -> list[dict]:
    breakdown: list[dict] = []
    for item in missing:
        field = item["field"]
        deduction = MISSING_INFO_PENALTIES.get(field)
        if not deduction:
            continue

        breakdown.append(
            {
                "category": f"Missing info: {field}",
                "evidence": item["reason"],
                "deduction": deduction,
                "explanation": (
                    f"{field} perlu diklarifikasi karena memengaruhi keputusan apply, "
                    "ekspektasi kerja, atau keamanan data pelamar."
                ),
            }
        )
    return breakdown

def _apply_score_caps(score: int, missing: list[dict], red_flags: list[dict]) -> int:
    capped_score = score
    missing_fields = _missing_fields(missing)
    if missing:
        capped_score = min(capped_score, 95)
    if missing_fields & CRITICAL_MISSING_FIELDS:
        capped_score = min(capped_score, 84)
    if any(flag["severity"] == "high" for flag in red_flags):
        capped_score = min(capped_score, 69)
    if any(flag["category"] in SEVERE_RISK_CAP_CATEGORIES for flag in red_flags):
        capped_score = min(capped_score, 44)
    return capped_score

def _missing_information(text: str) -> list[dict]:
    lowered = text.lower()
    checks = (
        (
            "Nama perusahaan",
            COMPANY_PATTERNS,
            "Lowongan tidak menyebutkan nama perusahaan, organisasi, atau domain resmi yang mudah diverifikasi.",
            "Apa nama perusahaan atau organisasi penyelenggara lowongan ini?",
        ),
        (
            "Posisi",
            POSITION_PATTERNS,
            "Lowongan belum menyebut posisi atau role dengan cukup jelas.",
            "Posisi apa yang sedang dibuka dan levelnya seperti apa?",
        ),
        (
            "Jenis lowongan",
            JOB_TYPE_PATTERNS,
            "Lowongan belum menjelaskan jenis kerja seperti magang, freelance, part-time, entry-level, atau kontrak.",
            "Apakah posisi ini magang, freelance, part-time, entry-level, atau kontrak?",
        ),
        (
            "Jobdesc",
            ROLE_DETAIL_PATTERNS,
            "Lowongan belum menjelaskan tanggung jawab, requirement, atau kualifikasi utama.",
            "Apa tiga tugas utama dan kualifikasi wajib untuk posisi ini?",
        ),
        (
            "Kompensasi",
            COMPENSATION_PATTERNS,
            "Lowongan tidak menyebutkan gaji, fee, honor, uang saku, insentif, atau bentuk kompensasi lain.",
            "Apakah posisi ini paid atau unpaid?",
        ),
        (
            "Jam kerja",
            WORK_TIME_PATTERNS,
            "Lowongan belum menyebut jam kerja, shift, atau estimasi waktu kerja.",
            "Berapa estimasi jam kerja per hari atau per minggu?",
        ),
        (
            "Durasi program",
            DURATION_PATTERNS,
            "Lowongan belum menyebut durasi program, periode kerja, tanggal mulai, atau tanggal selesai.",
            "Berapa durasi program atau kontrak kerja ini?",
        ),
        (
            "Work arrangement",
            WORK_ARRANGEMENT_PATTERNS,
            "Lowongan belum menyebut format kerja WFO, WFH, hybrid, remote, atau onsite.",
            "Format kerjanya WFO, WFH, hybrid, remote, atau onsite?",
        ),
        (
            "Lokasi kerja",
            LOCATION_PATTERNS,
            "Lowongan belum menyebut lokasi kerja atau alamat area kerja.",
            "Di mana lokasi kerja atau area penempatan posisi ini?",
        ),
        (
            "Benefit",
            BENEFIT_ONLY_PATTERNS,
            "Lowongan belum menyebut benefit, fasilitas, learning plan, sertifikat, portofolio, atau manfaat lain.",
            "Benefit konkret apa yang diterima pelamar jika bergabung?",
        ),
        (
            "Kontak resmi",
            CONTACT_PATTERNS,
            "Lowongan belum menyebut email, website, atau kanal kontak rekrutmen yang bisa diverifikasi.",
            "Kanal resmi apa yang digunakan untuk mengirim lamaran?",
        ),
        (
            "Supervisor/PIC",
            SUPERVISION_PATTERNS,
            "Lowongan belum menyebut supervisor, mentor, PIC, manager, atau penanggung jawab harian.",
            "Siapa supervisor, mentor, atau PIC harian untuk posisi ini?",
        ),
        (
            "Kontrak/perjanjian",
            CONTRACT_PATTERNS,
            "Lowongan belum menyebut kontrak, perjanjian, offer letter, atau dokumen kesepakatan kerja.",
            "Apakah ada kontrak, offer letter, atau perjanjian tertulis?",
        ),
        (
            "Syarat dokumen",
            DOCUMENT_REQUIREMENT_PATTERNS,
            "Lowongan belum menyebut dokumen apply seperti CV, portofolio, atau berkas pendukung.",
            "Dokumen apa saja yang perlu dikirim untuk apply?",
        ),
        (
            "Deadline apply",
            DEADLINE_PATTERNS,
            "Lowongan belum menyebut deadline pendaftaran atau batas pengiriman lamaran.",
            "Kapan batas akhir pendaftaran posisi ini?",
        ),
    )
    return [
        {
            "field": field,
            "status": "missing",
            "reason": reason,
            "question": question,
        }
        for field, patterns, reason, question in checks
        if not _contains_any(lowered, patterns)
    ]

def _positive_signals(text: str, source_platform: str) -> list[str]:
    lowered = text.lower()
    signals: list[str] = []
    if _contains_any(lowered, COMPANY_PATTERNS):
        signals.append("Identitas perusahaan atau organisasi mulai terlihat dan bisa diverifikasi.")
    if _contains_any(lowered, COMPENSATION_PATTERNS):
        signals.append("Ada informasi kompensasi, fee, gaji, atau uang saku.")
    if _contains_any(lowered, WORK_TIME_PATTERNS):
        signals.append("Ada informasi jam kerja, shift, atau format kerja.")
    if _contains_any(lowered, ROLE_DETAIL_PATTERNS):
        signals.append("Ada rincian tanggung jawab atau kualifikasi pekerjaan.")
    if _contains_any(lowered, DURATION_PATTERNS):
        signals.append("Durasi program atau kontrak kerja mulai dijelaskan.")
    if _contains_any(lowered, SUPERVISION_PATTERNS):
        signals.append("Ada petunjuk tentang mentor, supervisor, PIC, atau penanggung jawab.")
    if source_platform in {"linkedin", "job_site"}:
        signals.append("Sumber lowongan relatif mudah dibandingkan dengan kanal resmi perusahaan.")
    return signals or ["Belum banyak sinyal positif yang bisa dibaca dari teks ini."]

def _questions_to_ask(missing: list[dict], red_flags: list[dict], job_type: str) -> list[str]:
    questions: list[str] = []
    missing_fields = _missing_fields(missing)
    if "Kompensasi" in missing_fields:
        questions.append("Apakah posisi ini paid atau unpaid?")
    if "Jam kerja" in missing_fields:
        questions.append("Berapa estimasi jam kerja per minggu?")
    if "Nama perusahaan" in missing_fields:
        questions.append("Apakah ada website resmi atau profil perusahaan yang bisa dicek?")
    if "Durasi program" in missing_fields:
        questions.append("Berapa durasi program atau kontrak, dan kapan tanggal mulai serta selesai?")
    if "Supervisor/PIC" in missing_fields:
        questions.append("Siapa supervisor, mentor, atau PIC harian untuk posisi ini?")
    if "Work arrangement" in missing_fields:
        questions.append("Format kerjanya WFO, WFH, hybrid, remote, atau onsite?")
    if "Kontrak/perjanjian" in missing_fields:
        questions.append("Apakah ada kontrak, offer letter, atau perjanjian tertulis?")
    if "Deadline apply" in missing_fields:
        questions.append("Kapan batas akhir pendaftaran posisi ini?")

    categories = {flag["category"] for flag in red_flags}
    if "Meminta data pribadi sensitif terlalu awal" in categories:
        questions.append("Mengapa dokumen pribadi diperlukan di tahap awal?")
    if "Meminta biaya pendaftaran atau deposit" in categories:
        questions.append("Apakah ada alasan tertulis mengapa pelamar diminta membayar biaya atau deposit?")
    if "Jobdesc terlalu luas atau ambigu" in categories:
        questions.append("Apa prioritas tugas utama untuk posisi ini?")
    if "Benefit terlalu umum" in categories:
        questions.append("Apakah ada benefit lain seperti uang transport, insentif, atau learning plan?")
    if job_type == "internship":
        questions.append("Apakah ada mentor, learning plan, dan evaluasi akhir untuk program magang ini?")

    return _unique(questions)[:8]

def _recommended_action(score: int) -> str:
    if score >= 85:
        return "Apply"
    if score >= 70:
        return "Apply setelah klarifikasi"
    if score >= 45:
        return "Jangan apply dulu sebelum verifikasi"
    return "Hindari atau verifikasi secara ketat"

def _summary(score: int, risk_level: str, red_flags: list[dict]) -> str:
    if score >= 85:
        return f"Lowongan ini memiliki Trust Score tinggi dengan level {risk_level}. Tetap lakukan verifikasi dasar sebelum apply."
    if score >= 70:
        return f"Ada beberapa informasi yang perlu diverifikasi, tetapi indikasi risikonya belum dominan. Level saat ini: {risk_level}."
    if red_flags:
        top = red_flags[0]["category"].lower()
        return f"Terdapat indikasi risiko terkait {top}. Informasi lowongan perlu diperjelas sebelum kamu mengirim data atau melanjutkan proses."
    return f"Informasi belum cukup lengkap untuk dibaca dengan percaya diri. Level saat ini: {risk_level}."

def _risk_level(score: int) -> str:
    if score >= 85:
        return "Aman Dilamar"
    if score >= 70:
        return "Cukup Aman, Tapi Perlu Dicek"
    if score >= 45:
        return "Berisiko Sedang"
    return "Risiko Tinggi"

def _highlighted_terms(text: str, missing: list[dict]) -> list[dict]:
    highlights: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for rule in HIGHLIGHT_RULES:
        for pattern in rule.patterns:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                term = _squash(match.group(0))
                key = (term.lower(), rule.category)
                if key in seen:
                    continue
                seen.add(key)
                highlights.append(
                    {
                        "term": term,
                        "category": rule.category,
                        "severity": rule.severity,
                        "explanation": rule.explanation,
                    }
                )
    if "Nama perusahaan" in _missing_fields(missing):
        highlights.append(
            {
                "term": "perusahaan tidak disebutkan",
                "category": "Identitas perusahaan tidak cukup jelas",
                "severity": "high",
                "explanation": "Identitas perusahaan belum cukup jelas untuk diverifikasi dari teks.",
            }
        )
    return highlights[:20]

def _personal_data_warning(text: str) -> dict:
    detected: list[str] = []
    for pattern in PERSONAL_DATA_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            term = _squash(match.group(0))
            if term.lower() not in {item.lower() for item in detected}:
                detected.append(term)
    is_detected = bool(detected)
    return {
        "is_detected": is_detected,
        "detected_terms": detected,
        "message": (
            "Lowongan ini menyebut permintaan data pribadi atau pembayaran. Jangan mengirim KTP, rekening, OTP, password, atau membayar biaya apa pun sebelum identitas perusahaan dan proses rekrutmen jelas."
            if is_detected
            else ""
        ),
    }

def _safe_apply_checklist(missing: list[dict], red_flags: list[dict], personal_warning: dict) -> list[dict]:
    categories = {item["category"] for item in red_flags}
    missing_fields = _missing_fields(missing)

    def status(condition_passed: bool, warning_condition: bool = False) -> str:
        if condition_passed:
            return "passed"
        if warning_condition:
            return "warning"
        return "missing"

    return [
        {
            "item": "Identitas perusahaan jelas",
            "status": status("Nama perusahaan" not in missing_fields, "Identitas perusahaan tidak cukup jelas" in categories),
        },
        {
            "item": "Kontak recruiter profesional",
            "status": status("Kontak rekrutmen kurang profesional" not in categories, "Kontak rekrutmen kurang profesional" in categories),
        },
        {
            "item": "Jobdesc spesifik",
            "status": status("Jobdesc" not in missing_fields and "Jobdesc terlalu luas atau ambigu" not in categories, "Jobdesc terlalu luas atau ambigu" in categories),
        },
        {
            "item": "Kompensasi dijelaskan",
            "status": status("Kompensasi" not in missing_fields),
        },
        {
            "item": "Jam kerja jelas",
            "status": status("Jam kerja" not in missing_fields and "Jam fleksibel tanpa detail" not in categories, "Jam fleksibel tanpa detail" in categories),
        },
        {
            "item": "Tidak ada biaya pendaftaran",
            "status": status("Meminta biaya pendaftaran atau deposit" not in categories, "Meminta biaya pendaftaran atau deposit" in categories),
        },
        {
            "item": "Tidak diminta data pribadi sensitif terlalu awal",
            "status": status(not personal_warning["is_detected"], personal_warning["is_detected"]),
        },
        {
            "item": "Ada kontrak atau perjanjian kerja/magang",
            "status": status("Kontrak/perjanjian" not in missing_fields),
        },
        {
            "item": "Ada supervisor atau PIC yang jelas",
            "status": status("Supervisor/PIC" not in missing_fields),
        },
        {
            "item": "Durasi program disebutkan",
            "status": status("Durasi program" not in missing_fields),
        },
    ]

def _job_summary(text: str, job_type: str, source_platform: str, red_flags: list[dict]) -> dict:
    return {
        "position": _extract_position(text),
        "company": _extract_company(text),
        "job_type": job_type,
        "source_platform": source_platform,
        "compensation": _extract_field(text, COMPENSATION_PATTERNS),
        "working_hours": _extract_field(text, WORK_TIME_PATTERNS),
        "workload": _extract_field(text, WORKLOAD_PATTERNS),
        "benefits": _extract_field(text, BENEFIT_ONLY_PATTERNS),
        "contact": _extract_field(text, CONTACT_PATTERNS),
        "notes": _summary_note(red_flags),
    }

def _extract_position(text: str) -> str:
    patterns = (
        r"\b(?:membuka|dibuka|open recruitment|open position|lowongan)\b.{0,35}\b(?:posisi|untuk)?\s*([A-Za-z0-9 /&+-]{3,70})",
        r"\b(?:internship|magang|freelance|part.?time|entry.?level)\s+([A-Za-z0-9 /&+-]{3,60})",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _clean_field(match.group(1))
    first_line = _squash(text.split(".")[0])
    return first_line[:80] if first_line else "Belum jelas"

def _extract_company(text: str) -> str:
    match = re.search(r"\b((?:PT|CV|Yayasan|Universitas|Kampus|Studio|Agency)\s+[A-Za-z0-9 .&-]{2,60})", text)
    if match:
        return _clean_field(match.group(1))
    email = re.search(r"[A-Za-z0-9._%+-]+@([A-Za-z0-9.-]+\.[A-Za-z]{2,})", text)
    if email and email.group(1).lower() not in {"gmail.com", "yahoo.com", "hotmail.com"}:
        return email.group(1)
    return "Belum jelas"

def _extract_field(text: str, patterns: tuple[str, ...]) -> str:
    evidence = _first_evidence(text, patterns)
    return evidence or "Belum disebutkan"

def _summary_note(red_flags: list[dict]) -> str:
    if not red_flags:
        return "Informasi inti terlihat cukup baik, tetap verifikasi kanal resmi sebelum apply."
    top = ", ".join(item["category"] for item in red_flags[:3])
    return f"Perlu verifikasi pada: {top}."

def _first_evidence(text: str, patterns: tuple[str, ...]) -> str:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return _evidence_sentence(text, match.start(), match.end())
    return ""

def _evidence_sentence(text: str, match_start: int, match_end: int) -> str:
    previous_marks = [text.rfind(mark, 0, match_start) for mark in ".!?;"]
    previous = max(previous_marks)
    start = previous + 1 if previous >= 0 else 0

    next_marks = [text.find(mark, match_end) for mark in ".!?;"]
    next_candidates = [index for index in next_marks if index >= 0]
    end = min(next_candidates) + 1 if next_candidates else len(text)

    evidence = _squash(text[start:end]).strip(" .,;:-")
    if len(evidence) <= 180:
        return evidence

    start = max(0, match_start - 70)
    end = min(len(text), match_end + 70)
    while start > 0 and not text[start].isspace():
        start += 1
    while end < len(text) and not text[end - 1].isspace():
        end -= 1
    return f"...{_squash(text[start:end]).strip(' .,;:-')}..."

def _contains_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns)

def _clean_field(value: str) -> str:
    cleaned = _squash(value).strip(" .,;:-")
    return cleaned[:120] if cleaned else "Belum jelas"

def _missing_fields(missing: list[dict]) -> set[str]:
    return {str(item.get("field", "")) for item in missing}

def _missing_information_summary(missing: list[dict]) -> str:
    if not missing:
        return "Informasi utama pada lowongan ini sudah cukup lengkap. Tetap cocokkan identitas perusahaan dan kanal rekrutmen sebelum apply."

    fields = [item["field"] for item in missing[:5]]
    field_text = _join_labels(fields)
    if len(missing) <= 2:
        return (
            f"Sebagian besar informasi utama sudah tersedia, tetapi bagian {field_text} masih perlu diklarifikasi. "
            "Pastikan detail tersebut tertulis sebelum mengirim dokumen atau menerima tawaran."
        )

    if len(missing) <= 5:
        return (
            f"Lowongan ini belum menyebutkan beberapa bagian penting seperti {field_text}. "
            "Informasi tersebut berpengaruh pada keputusan apply karena berkaitan dengan ekspektasi kerja, risiko data pribadi, dan kejelasan proses."
        )

    return (
        f"Lowongan ini masih memiliki banyak informasi penting yang belum disebutkan, termasuk {field_text}. "
        "Sebaiknya lakukan klarifikasi terlebih dahulu sebelum mengirim CV, dokumen pribadi, atau menyetujui proses rekrutmen."
    )

def _join_labels(items: list[str]) -> str:
    if not items:
        return "informasi utama"
    if len(items) == 1:
        return items[0]
    return f"{', '.join(items[:-1])}, dan {items[-1]}"

def _clean_source_url(source_url: str | None) -> str | None:
    if source_url is None:
        return None
    cleaned = source_url.strip()
    return cleaned[:2048] if cleaned else None

def _clean_keywords(keywords: list[str]) -> list[str]:
    cleaned: list[str] = []
    seen: set[str] = set()
    for item in keywords:
        keyword = _squash(str(item)).strip(" ,;#")
        key = keyword.lower()
        if not keyword or key in seen:
            continue
        seen.add(key)
        cleaned.append(keyword[:60])
    return cleaned[:20]

def _squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def _unique(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
