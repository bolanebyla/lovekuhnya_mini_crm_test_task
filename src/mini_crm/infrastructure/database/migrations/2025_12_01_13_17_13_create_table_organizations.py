"""create table organizations

Revision ID: 986611ed8973
Revises:
Create Date: 2025-12-01 13:17:13.126666+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "986611ed8973"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organizations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organizations")),
        comment="Организации",
    )


def downgrade() -> None:
    op.drop_table("organizations")
