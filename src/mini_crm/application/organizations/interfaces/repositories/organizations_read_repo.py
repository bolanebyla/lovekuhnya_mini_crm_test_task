from typing import Protocol

from commons.entities import EntityId
from mini_crm.application.organizations.dtos import UserOrganisationDto


class OrganizationsReadRepo(Protocol):
    """Репозитория для чтения организаций"""

    async def get_list_by_member_user_id(
        self,
        user_id: EntityId,
    ) -> list[UserOrganisationDto]:
        """Получает список организаций, в которых состоит текущий пользователь"""
        ...
