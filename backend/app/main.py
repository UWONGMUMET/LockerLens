from collections import Counter

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, selectinload

from app import models
from app.config import get_settings
from app.database import get_db
from app.schemas import (
    ContactRequest,
    ContactResponse,
    DeleteResponse,
    ProfileStats,
    ScanHistoryDetail,
    ScanHistoryItem,
    ScanRequest,
    ScanResponse,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.security import (
    create_access_token,
    get_current_user,
    get_optional_user,
    hash_password,
    verify_password,
)
from app.services.scanner import analyze_job_text

settings = get_settings()

app = FastAPI(
    title="LokerLens API",
    description="Risk analysis API for digital job postings.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}

@app.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> dict:
    existing = db.scalar(select(models.User).where(models.User.email == str(payload.email).lower()))
    if existing:
        raise HTTPException(status_code=409, detail="Email sudah terdaftar.")

    user = models.User(
        name=payload.name.strip(),
        email=str(payload.email).lower(),
        hashed_password=hash_password(payload.password),
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email sudah terdaftar.") from exc
    return _user_response(user)

@app.post("/auth/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> dict:
    user = db.scalar(select(models.User).where(models.User.email == str(payload.email).lower()))
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email atau password tidak sesuai.")

    return {
        "access_token": create_access_token(str(user.id)),
        "token_type": "bearer",
        "user": _user_response(user),
    }

@app.get("/auth/me", response_model=UserResponse)
def me(current_user: models.User = Depends(get_current_user)) -> dict:
    return _user_response(current_user)

@app.post("/auth/logout", response_model=DeleteResponse)
def logout() -> DeleteResponse:
    return DeleteResponse(status="ok", message="Logout berhasil. Hapus token di client.")

@app.get("/auth/profile", response_model=ProfileStats)
def profile(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    stmt = (
        select(models.ScanResult)
        .join(models.JobPost)
        .where(models.JobPost.user_id == current_user.id)
        .order_by(desc(models.ScanResult.created_at))
    )
    scans = db.scalars(stmt).all()
    total = len(scans)
    average = round(sum(item.trust_score for item in scans) / total, 1) if total else None
    levels = Counter(item.risk_level for item in scans)
    high_risk = sum(1 for item in scans if item.trust_score <= 39)
    return {
        "user": _user_response(current_user),
        "total_scans": total,
        "average_trust_score": average,
        "most_common_risk_level": levels.most_common(1)[0][0] if levels else None,
        "high_risk_scans": high_risk,
        "joined_at": current_user.created_at,
    }

@app.post("/scan", response_model=ScanResponse)
def scan_job(
    payload: ScanRequest,
    db: Session = Depends(get_db),
    current_user: models.User | None = Depends(get_optional_user),
) -> dict:
    analysis = analyze_job_text(
        payload.job_text,
        payload.job_type,
        payload.source_platform,
        payload.source_url,
        payload.keywords,
    )

    if current_user is None:
        return analysis

    try:
        _save_scan(db, payload, analysis, current_user.id)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database belum tersedia. Pastikan PostgreSQL aktif dan migration sudah dijalankan.",
        ) from exc

    return analysis

@app.get("/scan/history", response_model=list[ScanHistoryItem])
def scan_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> list[dict]:
    limit = max(1, min(limit, 100))
    stmt = (
        select(models.ScanResult)
        .join(models.JobPost)
        .options(selectinload(models.ScanResult.job_post))
        .where(models.JobPost.user_id == current_user.id)
        .order_by(desc(models.ScanResult.created_at))
        .limit(limit)
    )
    results = db.scalars(stmt).all()
    return [_history_item(item) for item in results]

@app.get("/scan/history/{scan_id}", response_model=ScanHistoryDetail)
def scan_history_detail(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> dict:
    item = _get_user_scan_or_404(db, current_user.id, scan_id)
    return _scan_detail(item)

@app.delete("/scan/history/{scan_id}", response_model=DeleteResponse)
def delete_scan_history(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> DeleteResponse:
    item = _get_user_scan_or_404(db, current_user.id, scan_id)
    db.delete(item.job_post)
    db.commit()
    return DeleteResponse(status="deleted", message="Riwayat scan berhasil dihapus.")

@app.post("/contact", response_model=ContactResponse)
def create_contact_message(payload: ContactRequest, db: Session = Depends(get_db)) -> ContactResponse:
    message = models.ContactMessage(
        name=payload.name,
        email=str(payload.email),
        message=payload.message,
        category=payload.category,
    )
    try:
        db.add(message)
        db.commit()
        db.refresh(message)
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database belum tersedia. Pesan belum bisa disimpan.",
        ) from exc

    return ContactResponse(
        id=message.id,
        status="saved",
        message="Pesan berhasil disimpan. Terima kasih sudah menghubungi LokerLens.",
    )

def _save_scan(db: Session, payload: ScanRequest, analysis: dict, user_id: int) -> None:
    job_post = models.JobPost(
        user_id=user_id,
        job_text=payload.job_text,
        job_type=payload.job_type,
        source_platform=payload.source_platform,
        source_url=payload.source_url,
        keywords=payload.keywords,
    )
    scan_result = models.ScanResult(
        job_post=job_post,
        trust_score=analysis["trust_score"],
        risk_level=analysis["risk_level"],
        summary=analysis["summary"],
        job_summary=analysis["job_summary"],
        missing_information=analysis["missing_information"],
        missing_information_summary=analysis["missing_information_summary"],
        positive_signals=analysis["positive_signals"],
        questions_to_ask_recruiter=analysis["questions_to_ask_recruiter"],
        personal_data_warning=analysis["personal_data_warning"],
        recommended_action=analysis["recommended_action"],
        safety_note=analysis["safety_note"],
    )
    scan_result.red_flags = [models.RedFlag(**flag) for flag in analysis["red_flags"]]
    scan_result.highlighted_terms = [models.HighlightedTerm(**item) for item in analysis["highlighted_terms"]]
    scan_result.score_breakdown = [models.ScoreBreakdown(**item) for item in analysis["score_breakdown"]]
    scan_result.safe_apply_checklist = [
        models.SafeApplyChecklistItem(**item) for item in analysis["safe_apply_checklist"]
    ]
    db.add(job_post)
    db.add(scan_result)

def _get_user_scan_or_404(db: Session, user_id: int, scan_id: int) -> models.ScanResult:
    stmt = (
        select(models.ScanResult)
        .join(models.JobPost)
        .options(
            selectinload(models.ScanResult.job_post),
            selectinload(models.ScanResult.red_flags),
            selectinload(models.ScanResult.highlighted_terms),
            selectinload(models.ScanResult.score_breakdown),
            selectinload(models.ScanResult.safe_apply_checklist),
        )
        .where(models.ScanResult.id == scan_id, models.JobPost.user_id == user_id)
    )
    item = db.scalar(stmt)
    if item is None:
        raise HTTPException(status_code=404, detail="Riwayat scan tidak ditemukan.")
    return item

def _history_item(item: models.ScanResult) -> dict:
    preview = item.job_post.job_text.strip().replace("\n", " ")
    return {
        "id": item.id,
        "created_at": item.created_at,
        "job_type": item.job_post.job_type,
        "source_platform": item.job_post.source_platform,
        "source_url": item.job_post.source_url,
        "keywords_checked": item.job_post.keywords or [],
        "job_preview": preview[:180],
        "trust_score": item.trust_score,
        "risk_level": item.risk_level,
        "recommended_action": item.recommended_action,
    }

def _scan_detail(item: models.ScanResult) -> dict:
    missing_information = _normalize_missing_information(item.missing_information)
    return {
        "id": item.id,
        "created_at": item.created_at,
        "job_text": item.job_post.job_text,
        "job_type": item.job_post.job_type,
        "source_platform": item.job_post.source_platform,
        "source_url": item.job_post.source_url,
        "keywords_checked": item.job_post.keywords or [],
        "trust_score": item.trust_score,
        "risk_level": item.risk_level,
        "summary": item.summary,
        "job_summary": item.job_summary,
        "highlighted_terms": [
            {
                "term": term.term,
                "category": term.category,
                "severity": term.severity,
                "explanation": term.explanation,
            }
            for term in item.highlighted_terms
        ],
        "score_breakdown": [
            {
                "category": row.category,
                "evidence": row.evidence,
                "deduction": row.deduction,
                "explanation": row.explanation,
            }
            for row in item.score_breakdown
        ],
        "red_flags": [
            {
                "category": flag.category,
                "severity": flag.severity,
                "evidence": flag.evidence,
                "explanation": flag.explanation,
                "deduction": flag.deduction,
            }
            for flag in item.red_flags
        ],
        "missing_information": missing_information,
        "missing_information_summary": item.missing_information_summary
        or _fallback_missing_summary(missing_information),
        "positive_signals": item.positive_signals,
        "questions_to_ask_recruiter": item.questions_to_ask_recruiter,
        "recommended_action": item.recommended_action,
        "personal_data_warning": item.personal_data_warning,
        "safe_apply_checklist": [
            {"item": row.item, "status": row.status}
            for row in item.safe_apply_checklist
        ],
        "safety_note": item.safety_note,
    }

def _normalize_missing_information(items: list) -> list[dict]:
    normalized: list[dict] = []
    for item in items or []:
        if isinstance(item, dict):
            field = str(item.get("field") or "Informasi")
            reason = str(item.get("reason") or f"{field} belum disebutkan.")
            question = str(item.get("question") or f"Bisakah {field.lower()} dijelaskan?")
        else:
            text = str(item)
            field = _legacy_missing_field(text)
            reason = text
            question = f"Bisakah detail {field.lower()} dijelaskan?"

        normalized.append(
            {
                "field": field,
                "status": "missing",
                "reason": reason,
                "question": question,
            }
        )
    return normalized

def _legacy_missing_field(text: str) -> str:
    lowered = text.lower()
    if "perusahaan" in lowered:
        return "Nama perusahaan"
    if "kompensasi" in lowered or "gaji" in lowered or "uang saku" in lowered:
        return "Kompensasi"
    if "jam kerja" in lowered or "shift" in lowered:
        return "Jam kerja"
    if "lokasi" in lowered or "remote" in lowered or "hybrid" in lowered:
        return "Lokasi kerja"
    if "durasi" in lowered or "kontrak" in lowered or "periode" in lowered:
        return "Durasi program"
    if "supervisi" in lowered or "mentor" in lowered or "pic" in lowered:
        return "Supervisor/PIC"
    if "tanggung jawab" in lowered or "kualifikasi" in lowered:
        return "Jobdesc"
    return "Informasi"

def _fallback_missing_summary(missing_information: list[dict]) -> str:
    if not missing_information:
        return "Informasi utama pada lowongan ini sudah cukup lengkap."
    fields = ", ".join(item["field"] for item in missing_information[:4])
    if len(missing_information) <= 2:
        return f"Sebagian besar informasi utama sudah tersedia, tetapi bagian {fields} masih perlu diklarifikasi sebelum apply."
    return f"Lowongan ini masih belum menyebutkan beberapa informasi penting seperti {fields}. Klarifikasi detail tersebut sebelum mengirim data pribadi atau menerima tawaran."

def _user_response(user: models.User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at,
    }
