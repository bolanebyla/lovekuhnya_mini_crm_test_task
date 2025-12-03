from abc import abstractmethod
from typing import Protocol

from commons.entities import EntityId
from mini_crm.application.deals.entities import Deal


class DealsRepo(Protocol):
    """Репозитория для сделок"""

    @abstractmethod
    async def add(self, deal: Deal) -> None:
        """Добавляет сделку в хранилище"""
        ...

    @abstractmethod
    async def get_by_id(self, id_: EntityId) -> Deal | None:
        """Получает по id"""
        ...
