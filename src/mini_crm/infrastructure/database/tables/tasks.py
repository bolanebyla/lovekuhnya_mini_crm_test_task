from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    func,
)

from mini_crm.infrastructure.database.meta import metadata

tasks_table = Table(
    "tasks",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column(
        "deal_id",
        Integer,
        ForeignKey("deals.id"),
        nullable=False,
    ),
    Column(
        "title",
        String,
        nullable=False,
    ),
    Column(
        "description",
        Text,
        nullable=False,
        default="",
    ),
    Column(
        "due_date",
        Date,
        nullable=False,
    ),
    Column(
        "is_done",
        Boolean,
        nullable=False,
        default=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Index("ix_tasks_deal_is_done", "deal_id", "is_done"),
    Index("ix_tasks_deal_due_date", "deal_id", "due_date"),
    comment="Задачи по сделкам",
)
