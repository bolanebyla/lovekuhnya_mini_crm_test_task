"""create table activities

Revision ID: 254695ffdc5e
Revises: bbd6b8aeb48d
Create Date: 2025-12-04 02:26:22.657885+00:00

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "254695ffdc5e"
down_revision = "bbd6b8aeb48d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("deal_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["author_id"], ["users.id"], name=op.f("fk_activities_author_id_users")
        ),
        sa.ForeignKeyConstraint(
            ["deal_id"], ["deals.id"], name=op.f("fk_activities_deal_id_deals")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_activities")),
        comment="Активности по сделкам (таймлайн)",
    )
    op.create_index(op.f("ix_activities_deal_id"), "activities", ["deal_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_activities_deal_id"), table_name="activities")
    op.drop_table("activities")
