from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.activities.dtos import ActivityDto
from mini_crm.application.activities.interfaces import ActivitiesReadRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class GetActivitiesByDealUseCase:
    """Возвращает список активностей по сделке"""

    def __init__(
        self,
        operation: AsyncOperation,
        activities_read_repo: ActivitiesReadRepo,
    ):
        self._operation = operation
        self._activities_read_repo = activities_read_repo

    @async_operation
    async def execute(
        self,
        deal_id: EntityId,
        current_user: OrganizationMemberDto,
    ) -> list[ActivityDto]:
        return await self._activities_read_repo.get_by_organization_and_deal_id(
            organization_id=current_user.organization_id,
            deal_id=deal_id,
        )
