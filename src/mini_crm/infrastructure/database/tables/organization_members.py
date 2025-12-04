from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint, func

from mini_crm.infrastructure.database.meta import metadata

organization_members_table = Table(
    "organization_members",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "role",
        String,
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    UniqueConstraint("organization_id", "user_id"),
    comment="Участники организации",
)
