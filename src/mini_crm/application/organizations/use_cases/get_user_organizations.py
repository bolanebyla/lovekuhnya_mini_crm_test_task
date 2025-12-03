from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.organizations.dtos import UserOrganizationDto
from mini_crm.application.organizations.interfaces import OrganizationsReadRepo


class GetUserOrganizationsUseCase:
    """Возвращает список организаций, в которых состоит текущий пользователь"""

    def __init__(
        self,
        operation: AsyncOperation,
        organizations_read_repo: OrganizationsReadRepo,
    ):
        self._operation = operation
        self._organizations_read_repo = organizations_read_repo

    @async_operation
    async def execute(
        self,
        user_id: EntityId,
    ) -> list[UserOrganizationDto]:
        user_organizations = await self._organizations_read_repo.get_list_by_member_user_id(
            user_id=user_id
        )
        return user_organizations
