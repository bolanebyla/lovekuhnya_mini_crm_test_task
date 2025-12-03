from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Table, func

from mini_crm.infrastructure.database.meta import metadata

contacts_table = Table(
    "contacts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id"),
        index=True,
    ),
    Column(
        "owner_id",
        Integer,
        ForeignKey("users.id"),
        index=True,
    ),
    Column(
        "name",
        String,
        nullable=False,
    ),
    Column(
        "email",
        String,
        nullable=False,
    ),
    Column(
        "phone",
        String,
        nullable=False,
    ),
    Index(
        "ix_contacts_name_trgm",
        "name",
        postgresql_using="gin",
        postgresql_ops={"name": "gin_trgm_ops"},
    ),
    Index(
        "ix_contacts_email_trgm",
        "email",
        postgresql_using="gin",
        postgresql_ops={"email": "gin_trgm_ops"},
    ),
    comment="Контакты",
)
