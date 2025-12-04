from dataclasses import dataclass
from datetime import datetime

from commons.entities import EntityId


@dataclass(kw_only=True)
class User:
    """Пользователь"""

    id: EntityId | None = None
    email: str
    hashed_password: str
    name: str
    created_at: datetime
