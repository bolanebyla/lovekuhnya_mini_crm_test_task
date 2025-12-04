from dataclasses import dataclass
from datetime import date, datetime

from commons.entities import EntityId


@dataclass(kw_only=True)
class Task:
    """Задача по сделке"""

    id: EntityId | None = None
    deal_id: EntityId
    title: str
    description: str
    due_date: date
    is_done: bool
    created_at: datetime
