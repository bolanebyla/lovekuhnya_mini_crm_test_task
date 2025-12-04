from abc import abstractmethod
from typing import Protocol

from mini_crm.application.activities.entities import Activity


class ActivitiesRepo(Protocol):
    """Репозиторий для активностей"""

    @abstractmethod
    async def add(self, activity: Activity) -> None:
        """Добавляет активность в хранилище"""
        ...
