from typing import Any

from commons.datetime_utils import now_tz
from commons.entities import EntityId
from mini_crm.application.activities.entities import Activity
from mini_crm.application.activities.enums import ActivityTypes
from mini_crm.application.activities.interfaces import ActivitiesRepo


class ActivitiesService:
    """Сервис для работы с активностями"""

    def __init__(self, activities_repo: ActivitiesRepo):
        self._activities_repo = activities_repo

    async def create_activity(
        self,
        deal_id: EntityId,
        type_: ActivityTypes,
        payload: dict[str, Any],
        author_id: EntityId | None = None,
    ) -> None:
        """Создаёт активность"""
        activity = Activity(
            deal_id=deal_id,
            author_id=author_id,
            type=type_,
            payload=payload,
            created_at=now_tz(),
        )
        await self._activities_repo.add(activity=activity)

    async def create_status_changed_activity(
        self,
        deal_id: EntityId,
        old_status: str,
        new_status: str,
    ) -> None:
        """Создаёт активность изменения статуса"""
        await self.create_activity(
            deal_id=deal_id,
            type_=ActivityTypes.STATUS_CHANGED,
            payload={
                "old_status": old_status,
                "new_status": new_status,
            },
        )

    async def create_stage_changed_activity(
        self,
        deal_id: EntityId,
        old_stage: str,
        new_stage: str,
    ) -> None:
        """Создаёт активность изменения стадии"""
        await self.create_activity(
            deal_id=deal_id,
            type_=ActivityTypes.STAGE_CHANGED,
            payload={
                "old_stage": old_stage,
                "new_stage": new_stage,
            },
        )
