from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    job_posts: Mapped[list["JobPost"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

class JobPost(Base):
    __tablename__ = "job_posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    job_text: Mapped[str] = mapped_column(Text, nullable=False)
    job_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    source_platform: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    source_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    keywords: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User | None] = relationship(back_populates="job_posts")
    scan_results: Mapped[list[ScanResult]] = relationship(
        back_populates="job_post",
        cascade="all, delete-orphan",
    )

class ScanResult(Base):
    __tablename__ = "scan_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    job_post_id: Mapped[int] = mapped_column(ForeignKey("job_posts.id", ondelete="CASCADE"), index=True)
    trust_score: Mapped[int] = mapped_column(Integer, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(80), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    job_summary: Mapped[dict] = mapped_column(JSON, nullable=False)
    missing_information: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    missing_information_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    positive_signals: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    questions_to_ask_recruiter: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    personal_data_warning: Mapped[dict] = mapped_column(JSON, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    safety_note: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    job_post: Mapped[JobPost] = relationship(back_populates="scan_results")
    red_flags: Mapped[list[RedFlag]] = relationship(
        back_populates="scan_result",
        cascade="all, delete-orphan",
    )
    highlighted_terms: Mapped[list[HighlightedTerm]] = relationship(
        back_populates="scan_result",
        cascade="all, delete-orphan",
    )
    score_breakdown: Mapped[list[ScoreBreakdown]] = relationship(
        back_populates="scan_result",
        cascade="all, delete-orphan",
    )
    safe_apply_checklist: Mapped[list[SafeApplyChecklistItem]] = relationship(
        back_populates="scan_result",
        cascade="all, delete-orphan",
    )

class RedFlag(Base):
    __tablename__ = "red_flags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_result_id: Mapped[int] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        index=True,
    )
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    deduction: Mapped[int] = mapped_column(Integer, nullable=False)

    scan_result: Mapped[ScanResult] = relationship(back_populates="red_flags")

class HighlightedTerm(Base):
    __tablename__ = "highlighted_terms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_result_id: Mapped[int] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        index=True,
    )
    term: Mapped[str] = mapped_column(String(180), nullable=False)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    scan_result: Mapped[ScanResult] = relationship(back_populates="highlighted_terms")

class ScoreBreakdown(Base):
    __tablename__ = "score_breakdowns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_result_id: Mapped[int] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        index=True,
    )
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    evidence: Mapped[str] = mapped_column(Text, nullable=False)
    deduction: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)

    scan_result: Mapped[ScanResult] = relationship(back_populates="score_breakdown")

class SafeApplyChecklistItem(Base):
    __tablename__ = "safe_apply_checklist_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scan_result_id: Mapped[int] = mapped_column(
        ForeignKey("scan_results.id", ondelete="CASCADE"),
        index=True,
    )
    item: Mapped[str] = mapped_column(String(160), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    scan_result: Mapped[ScanResult] = relationship(back_populates="safe_apply_checklist")

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
