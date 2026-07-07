"""initial lokerlens schema

Revision ID: 0001_lokerlens
Revises:
Create Date: 2026-07-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_lokerlens"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.create_table(
        "job_posts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_text", sa.Text(), nullable=False),
        sa.Column("job_type", sa.String(length=32), nullable=False),
        sa.Column("source_platform", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_job_posts_id"), "job_posts", ["id"], unique=False)
    op.create_index(op.f("ix_job_posts_job_type"), "job_posts", ["job_type"], unique=False)
    op.create_index(op.f("ix_job_posts_source_platform"), "job_posts", ["source_platform"], unique=False)

    op.create_table(
        "contact_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_contact_messages_email"), "contact_messages", ["email"], unique=False)
    op.create_index(op.f("ix_contact_messages_id"), "contact_messages", ["id"], unique=False)

    op.create_table(
        "scan_results",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("job_post_id", sa.Integer(), nullable=False),
        sa.Column("trust_score", sa.Integer(), nullable=False),
        sa.Column("risk_level", sa.String(length=80), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("missing_information", sa.JSON(), nullable=False),
        sa.Column("positive_signals", sa.JSON(), nullable=False),
        sa.Column("questions_to_ask_recruiter", sa.JSON(), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("safety_note", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["job_post_id"], ["job_posts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scan_results_id"), "scan_results", ["id"], unique=False)
    op.create_index(op.f("ix_scan_results_job_post_id"), "scan_results", ["job_post_id"], unique=False)

    op.create_table(
        "red_flags",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scan_result_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("deduction", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["scan_result_id"], ["scan_results.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_red_flags_id"), "red_flags", ["id"], unique=False)
    op.create_index(op.f("ix_red_flags_scan_result_id"), "red_flags", ["scan_result_id"], unique=False)

def downgrade() -> None:
    op.drop_index(op.f("ix_red_flags_scan_result_id"), table_name="red_flags")
    op.drop_index(op.f("ix_red_flags_id"), table_name="red_flags")
    op.drop_table("red_flags")
    op.drop_index(op.f("ix_scan_results_job_post_id"), table_name="scan_results")
    op.drop_index(op.f("ix_scan_results_id"), table_name="scan_results")
    op.drop_table("scan_results")
    op.drop_index(op.f("ix_contact_messages_id"), table_name="contact_messages")
    op.drop_index(op.f("ix_contact_messages_email"), table_name="contact_messages")
    op.drop_table("contact_messages")
    op.drop_index(op.f("ix_job_posts_source_platform"), table_name="job_posts")
    op.drop_index(op.f("ix_job_posts_job_type"), table_name="job_posts")
    op.drop_index(op.f("ix_job_posts_id"), table_name="job_posts")
    op.drop_table("job_posts")
