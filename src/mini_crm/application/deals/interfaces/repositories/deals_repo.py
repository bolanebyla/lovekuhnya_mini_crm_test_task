from abc import abstractmethod
from typing import Protocol

from mini_crm.application.deals.entities import Deal


class DealsRepo(Protocol):
    """Репозитория для сделок"""

    @abstractmethod
    async def add(self, deal: Deal) -> None:
        """Добавляет сделку в хранилище"""
        ...
