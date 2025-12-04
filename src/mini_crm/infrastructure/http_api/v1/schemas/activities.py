from datetime import datetime
from typing import Any

from pydantic import BaseModel

from mini_crm.application.activities.dtos import ActivityDto
from mini_crm.application.activities.enums import ActivityTypes


class ActivityShortSchema(BaseModel):
    """Информация по активности"""

    id: int
    deal_id: int
    author_id: int | None
    type: ActivityTypes
    payload: dict[str, Any]
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: ActivityDto) -> "ActivityShortSchema":
        return cls(
            id=dto.id,
            deal_id=dto.deal_id,
            author_id=dto.author_id,
            type=dto.type,
            payload=dto.payload,
            created_at=dto.created_at,
        )
