"""auth and scan detail schema

Revision ID: 0002_auth_scan_detail
Revises: 0001_lokerlens
Create Date: 2026-07-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_auth_scan_detail"
down_revision: str | None = "0001_lokerlens"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=180), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.add_column("job_posts", sa.Column("user_id", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_job_posts_user_id"), "job_posts", ["user_id"], unique=False)
    op.create_foreign_key(
        "fk_job_posts_user_id_users",
        "job_posts",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.add_column("scan_results", sa.Column("job_summary", sa.JSON(), nullable=True))
    op.add_column("scan_results", sa.Column("personal_data_warning", sa.JSON(), nullable=True))
    op.execute("UPDATE scan_results SET job_summary = '{}' WHERE job_summary IS NULL")
    op.execute("UPDATE scan_results SET personal_data_warning = '{}' WHERE personal_data_warning IS NULL")

    op.create_table(
        "highlighted_terms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scan_result_id", sa.Integer(), nullable=False),
        sa.Column("term", sa.String(length=180), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["scan_result_id"], ["scan_results.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_highlighted_terms_id"), "highlighted_terms", ["id"], unique=False)
    op.create_index(op.f("ix_highlighted_terms_scan_result_id"), "highlighted_terms", ["scan_result_id"], unique=False)

    op.create_table(
        "score_breakdowns",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scan_result_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(length=120), nullable=False),
        sa.Column("evidence", sa.Text(), nullable=False),
        sa.Column("deduction", sa.Integer(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["scan_result_id"], ["scan_results.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_score_breakdowns_id"), "score_breakdowns", ["id"], unique=False)
    op.create_index(op.f("ix_score_breakdowns_scan_result_id"), "score_breakdowns", ["scan_result_id"], unique=False)

    op.create_table(
        "safe_apply_checklist_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("scan_result_id", sa.Integer(), nullable=False),
        sa.Column("item", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["scan_result_id"], ["scan_results.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_safe_apply_checklist_items_id"), "safe_apply_checklist_items", ["id"], unique=False)
    op.create_index(
        op.f("ix_safe_apply_checklist_items_scan_result_id"),
        "safe_apply_checklist_items",
        ["scan_result_id"],
        unique=False,
    )

def downgrade() -> None:
    op.drop_index(op.f("ix_safe_apply_checklist_items_scan_result_id"), table_name="safe_apply_checklist_items")
    op.drop_index(op.f("ix_safe_apply_checklist_items_id"), table_name="safe_apply_checklist_items")
    op.drop_table("safe_apply_checklist_items")
    op.drop_index(op.f("ix_score_breakdowns_scan_result_id"), table_name="score_breakdowns")
    op.drop_index(op.f("ix_score_breakdowns_id"), table_name="score_breakdowns")
    op.drop_table("score_breakdowns")
    op.drop_index(op.f("ix_highlighted_terms_scan_result_id"), table_name="highlighted_terms")
    op.drop_index(op.f("ix_highlighted_terms_id"), table_name="highlighted_terms")
    op.drop_table("highlighted_terms")
    op.drop_column("scan_results", "personal_data_warning")
    op.drop_column("scan_results", "job_summary")
    op.drop_constraint("fk_job_posts_user_id_users", "job_posts", type_="foreignkey")
    op.drop_index(op.f("ix_job_posts_user_id"), table_name="job_posts")
    op.drop_column("job_posts", "user_id")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
