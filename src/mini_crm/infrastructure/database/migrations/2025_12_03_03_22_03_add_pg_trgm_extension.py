"""add pg_trgm extension

Revision ID: 0561df532f3d
Revises: 45d07c5c273c
Create Date: 2025-12-03 03:22:03.530001+00:00

"""

from alembic import op

revision = "0561df532f3d"
down_revision = "45d07c5c273c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


def downgrade() -> None:
    pass
