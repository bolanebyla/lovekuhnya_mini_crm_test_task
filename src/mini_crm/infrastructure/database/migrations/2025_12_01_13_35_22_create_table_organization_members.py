"""create table organization_members

Revision ID: 45d07c5c273c
Revises: 33ea8dc44d9d
Create Date: 2025-12-01 13:35:22.374260+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "45d07c5c273c"
down_revision = "33ea8dc44d9d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organization_members",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name=op.f("fk_organization_members_organization_id_organizations"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_organization_members_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_organization_members")),
        sa.UniqueConstraint(
            "organization_id", "user_id", name=op.f("uq_organization_members_organization_id")
        ),
        comment="Члены организации",
    )
    op.create_index(
        op.f("ix_organization_members_user_id"), "organization_members", ["user_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_organization_members_user_id"), table_name="organization_members")
    op.drop_table("organization_members")
