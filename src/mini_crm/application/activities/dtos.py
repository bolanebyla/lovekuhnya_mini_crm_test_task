from dataclasses import dataclass
from datetime import datetime
from typing import Any

from commons.entities import EntityId
from mini_crm.application.activities.enums import ActivityTypes


@dataclass(kw_only=True)
class ActivityDto:
    """Информация по активности"""

    id: EntityId
    deal_id: EntityId
    author_id: EntityId | None
    type: ActivityTypes
    payload: dict[str, Any]
    created_at: datetime
