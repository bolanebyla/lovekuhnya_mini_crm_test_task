"""create table tasks

Revision ID: bbd6b8aeb48d
Revises: 0f7685911cde
Create Date: 2025-12-04 02:22:22.893858+00:00

"""

import sqlalchemy as sa
from alembic import op

revision = "bbd6b8aeb48d"
down_revision = "0f7685911cde"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("deal_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("due_date", sa.Date, nullable=False),
        sa.Column("is_done", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["deal_id"], ["deals.id"], name=op.f("fk_tasks_deal_id_deals")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tasks")),
        comment="Задачи по сделкам",
    )
    op.create_index(op.f("ix_tasks_deal_id"), "tasks", ["deal_id"], unique=False)
    op.create_index(op.f("ix_tasks_due_date"), "tasks", ["due_date"], unique=False)
    op.create_index(op.f("ix_tasks_is_done"), "tasks", ["is_done"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_tasks_is_done"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_due_date"), table_name="tasks")
    op.drop_index(op.f("ix_tasks_deal_id"), table_name="tasks")
    op.drop_table("tasks")
