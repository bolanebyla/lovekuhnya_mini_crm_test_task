from abc import abstractmethod
from typing import Protocol

from mini_crm.application.organizations.entities import Organization


class OrganizationsRepo(Protocol):
    """Репозиторий для организаций"""

    @abstractmethod
    async def add(self, organization: Organization) -> None:
        """Добавляет организацию в хранилище"""
        ...

    @abstractmethod
    async def get_by_name(self, name: str) -> Organization | None:
        """Получает организацию по названию"""
        ...
