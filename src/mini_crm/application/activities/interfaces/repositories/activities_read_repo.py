from abc import abstractmethod
from typing import Protocol

from commons.entities import EntityId
from mini_crm.application.activities.dtos import ActivityDto


class ActivitiesReadRepo(Protocol):
    """Репозиторий для чтения активностей"""

    @abstractmethod
    async def get_by_organization_and_deal_id(
        self,
        organization_id: EntityId,
        deal_id: EntityId,
    ) -> list[ActivityDto]:
        """Получает список активностей по сделке"""
        ...
