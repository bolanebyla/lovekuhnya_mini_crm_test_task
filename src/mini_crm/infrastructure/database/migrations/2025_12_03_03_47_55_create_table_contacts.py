"""create table contacts

Revision ID: dd651f8c03d7
Revises: 0561df532f3d
Create Date: 2025-12-03 03:47:55.763935+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "dd651f8c03d7"
down_revision = "0561df532f3d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "contacts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("organization_id", sa.Integer(), nullable=True),
        sa.Column("owner_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["organization_id"],
            ["organizations.id"],
            name=op.f("fk_contacts_organization_id_organizations"),
        ),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name=op.f("fk_contacts_owner_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contacts")),
        comment="Контакты",
    )
    op.create_index(
        "ix_contacts_email_trgm",
        "contacts",
        ["email"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"email": "gin_trgm_ops"},
    )
    op.create_index(
        "ix_contacts_name_trgm",
        "contacts",
        ["name"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    )
    op.create_index(
        op.f("ix_contacts_organization_id"), "contacts", ["organization_id"], unique=False
    )
    op.create_index(op.f("ix_contacts_owner_id"), "contacts", ["owner_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_contacts_owner_id"), table_name="contacts")
    op.drop_index(op.f("ix_contacts_organization_id"), table_name="contacts")
    op.drop_index(
        "ix_contacts_name_trgm",
        table_name="contacts",
    )
    op.drop_index(
        "ix_contacts_email_trgm",
        table_name="contacts",
    )
    op.drop_table("contacts")
