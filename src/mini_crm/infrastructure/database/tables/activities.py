from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.dialects.postgresql import JSONB

from mini_crm.infrastructure.database.meta import metadata

activities_table = Table(
    "activities",
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
        "author_id",
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    ),
    Column(
        "type",
        String,
        nullable=False,
    ),
    Column(
        "payload",
        JSONB,
        nullable=False,
        default={},
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    comment="Активности по сделкам (таймлайн)",
)
