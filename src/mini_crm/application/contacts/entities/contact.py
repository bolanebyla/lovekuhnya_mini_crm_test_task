from dataclasses import dataclass
from datetime import datetime

from commons.entities import EntityId


@dataclass(kw_only=True)
class Contact:
    """Контакт"""

    id: EntityId | None = None
    created_at: datetime
    organization_id: EntityId
    owner_id: EntityId
    name: str
    email: str
    phone: str
