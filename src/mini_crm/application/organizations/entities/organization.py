from dataclasses import dataclass
from datetime import datetime

from commons.entities import EntityId


@dataclass(kw_only=True)
class Organization:
    """Организация"""

    id: EntityId
    created_at: datetime
