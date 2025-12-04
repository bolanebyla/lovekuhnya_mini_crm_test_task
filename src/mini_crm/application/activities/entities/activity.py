from dataclasses import dataclass
from datetime import datetime
from typing import Any

from commons.entities import EntityId
from mini_crm.application.activities.enums import ActivityTypes


@dataclass(kw_only=True)
class Activity:
    """Активность по сделке (таймлайн)"""

    id: EntityId | None = None
    deal_id: EntityId
    author_id: EntityId | None = None
    """Id автора (User), может быть null для системных событий"""
    type: ActivityTypes
    payload: dict[str, Any]
    """Произвольные детали активности в формате JSON"""
    created_at: datetime
