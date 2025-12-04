from typing import Any

from mini_crm.application.activities.dtos import CreateActivityDto
from mini_crm.application.activities.enums import ActivityTypes


def create_activity_dto(
    type_: ActivityTypes = ActivityTypes.COMMENT,
    payload: dict[str, Any] | None = None,
) -> CreateActivityDto:
    return CreateActivityDto(
        type=type_,
        payload=payload or {"text": "Test comment"},
    )
