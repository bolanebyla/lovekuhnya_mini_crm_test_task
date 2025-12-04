from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, Numeric, String, Table, func

from mini_crm.infrastructure.database.meta import metadata

deals_table = Table(
    "deals",
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
        "contact_id",
        Integer,
        ForeignKey("contacts.id"),
    ),
    Column(
        "owner_id",
        Integer,
        ForeignKey("users.id"),
    ),
    Column(
        "title",
        String,
        nullable=False,
    ),
    Column(
        "amount",
        Numeric(20, 2),
        nullable=False,
    ),
    Column(
        "currency",
        String,
        nullable=False,
    ),
    Column(
        "status",
        String,
        nullable=False,
    ),
    Column(
        "stage",
        String,
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    ),
    Index("ix_deals_org_status", "organization_id", "status"),
    Index("ix_deals_org_created_at", "organization_id", "created_at"),
    Index("ix_deals_org_owner", "organization_id", "owner_id"),
    comment="Сделки",
)
