from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

JobType = Literal["internship", "freelance", "part_time", "entry_level"]
SourcePlatform = Literal["instagram", "linkedin", "twitter", "telegram", "job_site", "other"]
Severity = Literal["low", "medium", "high"]
ChecklistStatus = Literal["passed", "warning", "missing"]
ContactCategory = Literal["feedback", "campus_partnership", "employer_verification", "other"]

class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class ProfileStats(BaseModel):
    user: UserResponse
    total_scans: int
    average_trust_score: float | None
    most_common_risk_level: str | None
    high_risk_scans: int
    joined_at: datetime

class ScanRequest(BaseModel):
    job_text: str = Field(..., min_length=20, max_length=12000)
    job_type: JobType
    source_platform: SourcePlatform
    source_url: str | None = Field(default=None, max_length=2048)
    keywords: list[str] = Field(default_factory=list, max_length=20)

    @field_validator("source_url")
    @classmethod
    def normalize_source_url(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    @field_validator("keywords")
    @classmethod
    def normalize_keywords(cls, value: list[str]) -> list[str]:
        cleaned: list[str] = []
        seen: set[str] = set()
        for item in value:
            keyword = item.strip()
            key = keyword.lower()
            if not keyword or key in seen:
                continue
            seen.add(key)
            cleaned.append(keyword[:60])
        return cleaned[:20]

class JobSummary(BaseModel):
    position: str
    company: str
    job_type: str
    source_platform: str
    compensation: str
    working_hours: str
    workload: str
    benefits: str
    contact: str
    notes: str

class HighlightedTermResult(BaseModel):
    term: str
    category: str
    severity: Severity
    explanation: str

class ScoreBreakdownItem(BaseModel):
    category: str
    evidence: str
    deduction: int
    explanation: str

class RedFlagResult(BaseModel):
    category: str
    severity: Severity
    evidence: str
    explanation: str
    deduction: int

class PersonalDataWarning(BaseModel):
    is_detected: bool
    detected_terms: list[str]
    message: str

class SafeApplyChecklistItem(BaseModel):
    item: str
    status: ChecklistStatus

class MissingInformationItem(BaseModel):
    field: str
    status: Literal["missing"] = "missing"
    reason: str
    question: str

class ScanResponse(BaseModel):
    trust_score: int
    risk_level: str
    summary: str
    job_type: str
    source_platform: str
    source_url: str | None = None
    keywords_checked: list[str] = Field(default_factory=list)
    job_summary: JobSummary
    highlighted_terms: list[HighlightedTermResult]
    score_breakdown: list[ScoreBreakdownItem]
    red_flags: list[RedFlagResult]
    missing_information: list[MissingInformationItem]
    missing_information_summary: str
    positive_signals: list[str]
    questions_to_ask_recruiter: list[str]
    recommended_action: str
    personal_data_warning: PersonalDataWarning
    safe_apply_checklist: list[SafeApplyChecklistItem]
    safety_note: str

class ScanHistoryItem(BaseModel):
    id: int
    created_at: datetime
    job_type: str
    source_platform: str
    source_url: str | None = None
    keywords_checked: list[str] = Field(default_factory=list)
    job_preview: str
    trust_score: int
    risk_level: str
    recommended_action: str

class ScanHistoryDetail(ScanResponse):
    id: int
    created_at: datetime
    job_text: str

class DeleteResponse(BaseModel):
    status: str
    message: str

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=3000)
    category: ContactCategory

class ContactResponse(BaseModel):
    id: int
    status: str
    message: str
