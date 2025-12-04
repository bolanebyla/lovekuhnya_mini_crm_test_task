"""add_indexes

Revision ID: 9673e234433d
Revises: 254695ffdc5e
Create Date: 2025-12-04 08:57:53.368203+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "9673e234433d"
down_revision = "254695ffdc5e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("contacts", "organization_id", existing_type=sa.INTEGER(), nullable=False)
    op.drop_index(op.f("ix_contacts_owner_id"), table_name="contacts")
    op.create_index(
        "ix_contacts_org_owner", "contacts", ["organization_id", "owner_id"], unique=False
    )
    op.alter_column("deals", "organization_id", existing_type=sa.INTEGER(), nullable=False)
    op.drop_index(op.f("ix_deals_amount"), table_name="deals")
    op.drop_index(op.f("ix_deals_contact_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_created_at"), table_name="deals")
    op.drop_index(op.f("ix_deals_organization_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_owner_id"), table_name="deals")
    op.drop_index(op.f("ix_deals_stage"), table_name="deals")
    op.drop_index(op.f("ix_deals_status"), table_name="deals")
    op.create_index(
        "ix_deals_org_created_at", "deals", ["organization_id", "created_at"], unique=False
    )
    op.create_index("ix_deals_org_owner", "deals", ["organization_id", "owner_id"], unique=False)
    op.create_index("ix_deals_org_status", "deals", ["organization_id", "status"], unique=False)
    op.add_column(
        "organization_members",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.alter_column(
        "organization_members", "organization_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column("organization_members", "user_id", existing_type=sa.INTEGER(), nullable=False)
    op.create_index(op.f("ix_organizations_name"), "organizations", ["name"], unique=False)
    op.drop_index(op.f("ix_tasks_deal_id"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_due_date"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_is_done"), table_name="tasks")
    op.create_index("ix_tasks_deal_due_date", "tasks", ["deal_id", "due_date"], unique=False)
    op.create_index("ix_tasks_deal_is_done", "tasks", ["deal_id", "is_done"], unique=False)
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_name"), table_name="users")
    op.create_unique_constraint(op.f("uq_users_email"), "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_email"), "users", type_="unique")
    op.create_index(op.f("ix_users_name"), "users", ["name"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.drop_index("ix_tasks_deal_is_done", table_name="tasks")
    op.drop_index("ix_tasks_deal_due_date", table_name="tasks")
    op.create_index(op.f("ix_tasks_is_done"), "tasks", ["is_done"], unique=False)
    op.create_index(op.f("ix_tasks_due_date"), "tasks", ["due_date"], unique=False)
    op.create_index(op.f("ix_tasks_deal_id"), "tasks", ["deal_id"], unique=False)
    op.drop_index(op.f("ix_organizations_name"), table_name="organizations")
    op.alter_column("organization_members", "user_id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column(
        "organization_members", "organization_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.drop_column("organization_members", "created_at")
    op.drop_index("ix_deals_org_status", table_name="deals")
    op.drop_index("ix_deals_org_owner", table_name="deals")
    op.drop_index("ix_deals_org_created_at", table_name="deals")
    op.create_index(op.f("ix_deals_status"), "deals", ["status"], unique=False)
    op.create_index(op.f("ix_deals_stage"), "deals", ["stage"], unique=False)
    op.create_index(op.f("ix_deals_owner_id"), "deals", ["owner_id"], unique=False)
    op.create_index(op.f("ix_deals_organization_id"), "deals", ["organization_id"], unique=False)
    op.create_index(op.f("ix_deals_created_at"), "deals", ["created_at"], unique=False)
    op.create_index(op.f("ix_deals_contact_id"), "deals", ["contact_id"], unique=False)
    op.create_index(op.f("ix_deals_amount"), "deals", ["amount"], unique=False)
    op.alter_column("deals", "organization_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_index("ix_contacts_org_owner", table_name="contacts")
    op.create_index(op.f("ix_contacts_owner_id"), "contacts", ["owner_id"], unique=False)
    op.alter_column("contacts", "organization_id", existing_type=sa.INTEGER(), nullable=True)
