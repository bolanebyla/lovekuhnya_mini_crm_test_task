from sqlalchemy import Column, DateTime, Integer, String, Table, func

from mini_crm.infrastructure.database.meta import metadata

organizations_table = Table(
    "organizations",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column(
        "name",
        String,
        nullable=False,
        index=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    comment="Организации",
)
