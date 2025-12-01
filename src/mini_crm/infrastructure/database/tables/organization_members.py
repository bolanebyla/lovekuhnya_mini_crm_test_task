from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint

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
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("users.id"),
        index=True,
    ),
    Column(
        "role",
        String,
        nullable=False,
    ),
    UniqueConstraint("organization_id", "user_id"),
    comment="Члены организации",
)
