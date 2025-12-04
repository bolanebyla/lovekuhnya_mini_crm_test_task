from abc import abstractmethod
from typing import Protocol

from mini_crm.application.organizations.entities import OrganizationMember


class OrganizationMembersRepo(Protocol):
    """Репозиторий для участников организации"""

    @abstractmethod
    async def add(self, organization_member: OrganizationMember) -> None:
        """Добавляет участника организации в хранилище"""
        ...
