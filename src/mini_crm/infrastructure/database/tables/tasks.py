from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
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
        index=True,
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
        index=True,
    ),
    Column(
        "is_done",
        Boolean,
        nullable=False,
        default=False,
        index=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    comment="Задачи по сделкам",
)
