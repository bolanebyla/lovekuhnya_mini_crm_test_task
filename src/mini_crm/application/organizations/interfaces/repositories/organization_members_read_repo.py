from abc import abstractmethod
from typing import Protocol

from commons.entities import EntityId
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class OrganizationMembersReadRepo(Protocol):
    """Репозитория для чтения членов организации"""

    @abstractmethod
    async def get_by_organization_and_user_id(
        self,
        organization_id: EntityId,
        user_id: EntityId,
    ) -> OrganizationMemberDto | None:
        """Получает информацию о членстве пользователя в организации"""
        ...
