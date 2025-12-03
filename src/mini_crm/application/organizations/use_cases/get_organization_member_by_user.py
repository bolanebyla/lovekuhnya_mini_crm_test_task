from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.errors import (
    OrganizationMemberNotFoundByOrganizationIdAndUserId,
)
from mini_crm.application.organizations.interfaces import (
    OrganizationMembersReadRepo,
)


class GetOrganizationMemberByUserUseCase:
    """Возвращает информацию об участнике организации"""

    def __init__(
        self,
        operation: AsyncOperation,
        organization_members_read_repo: OrganizationMembersReadRepo,
    ):
        self._operation = operation
        self._organization_members_read_repo = organization_members_read_repo

    @async_operation
    async def execute(
        self,
        organization_id: EntityId,
        user_id: EntityId,
    ) -> OrganizationMemberDto:
        organization_member_dto = (
            await self._organization_members_read_repo.get_by_organization_and_user_id(
                organization_id=organization_id,
                user_id=user_id,
            )
        )

        if organization_member_dto is None:
            raise OrganizationMemberNotFoundByOrganizationIdAndUserId(
                organization_id=organization_id,
                user_id=user_id,
            )

        return organization_member_dto
