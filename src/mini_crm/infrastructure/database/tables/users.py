from sqlalchemy import Column, DateTime, Integer, String, Table, func

from mini_crm.infrastructure.database.meta import metadata

users_table = Table(
    "users",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column(
        "email",
        String,
        nullable=False,
        unique=True,
        index=True,
    ),
    Column(
        "hashed_password",
        String,
        nullable=False,
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
    comment="Пользователи",
)
