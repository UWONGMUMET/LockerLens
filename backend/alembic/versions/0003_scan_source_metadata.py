"""scan source metadata

Revision ID: 0003_scan_source_metadata
Revises: 0002_auth_scan_detail
Create Date: 2026-07-07
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_scan_source_metadata"
down_revision: str | None = "0002_auth_scan_detail"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

def upgrade() -> None:
    op.add_column("job_posts", sa.Column("source_url", sa.String(length=2048), nullable=True))
    op.add_column("job_posts", sa.Column("keywords", sa.JSON(), nullable=True))
    op.add_column("scan_results", sa.Column("missing_information_summary", sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column("scan_results", "missing_information_summary")
    op.drop_column("job_posts", "keywords")
    op.drop_column("job_posts", "source_url")
