"""create table deals

Revision ID: 0f7685911cde
Revises: dd651f8c03d7
Create Date: 2025-12-03 09:09:55.025629+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "0f7685911cde"
down_revision = "dd651f8c03d7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "deals",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=True),
        sa.Column("contact_id", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=20, scale=2), nullable=False),
        sa.Column("currency", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("stage", sa.String(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"], ["contacts.id"], name=op.f("fk_deals_contact_id_contacts")
        ),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name=op.f("fk_deals_organization_id_organizations"),
        ),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], name=op.f("fk_deals_owner_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_deals")),
        comment="Сделки",
    )
    op.create_index(op.f("ix_deals_amount"), "deals", ["amount"], unique=False)
    op.create_index(op.f("ix_deals_contact_id"), "deals", ["contact_id"], unique=False)
    op.create_index(op.f("ix_deals_created_at"), "deals", ["created_at"], unique=False)
    op.create_index(op.f("ix_deals_organization_id"), "deals", ["organization_id"], unique=False)
    op.create_index(op.f("ix_deals_owner_id"), "deals", ["owner_id"], unique=False)
    op.create_index(op.f("ix_deals_stage"), "deals", ["stage"], unique=False)
    op.create_index(op.f("ix_deals_status"), "deals", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_deals_status"), table_name="deals")
    op.drop_index(op.f("ix_deals_stage"), table_name="deals")
    op.drop_index(op.f("ix_deals_owner_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_organization_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_created_at"), table_name="deals")
    op.drop_index(op.f("ix_deals_contact_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_amount"), table_name="deals")
    op.drop_table("deals")
