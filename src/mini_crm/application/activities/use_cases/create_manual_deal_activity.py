from commons.datetime_utils import now_tz
from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.activities.dtos import CreateActivityDto
from mini_crm.application.activities.entities import Activity
from mini_crm.application.activities.enums import ActivityTypes
from mini_crm.application.activities.errors import OnlyCommentActivityTypeAllowedError
from mini_crm.application.activities.interfaces import ActivitiesRepo
from mini_crm.application.deals.services import DealsService
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class CreateManualDealActivityUseCase:
    """Создать активность вручную (только comment)"""

    def __init__(
        self,
        operation: AsyncOperation,
        activities_repo: ActivitiesRepo,
        deals_service: DealsService,
    ):
        self._operation = operation
        self._activities_repo = activities_repo
        self._deals_service = deals_service

    @async_operation
    async def execute(
        self,
        deal_id: EntityId,
        create_dto: CreateActivityDto,
        current_user: OrganizationMemberDto,
    ) -> None:
        if create_dto.type != ActivityTypes.COMMENT:
            raise OnlyCommentActivityTypeAllowedError()

        await self._deals_service.check_deal_access(
            deal_id=deal_id,
            current_user=current_user,
        )

        activity = Activity(
            deal_id=deal_id,
            author_id=current_user.user_id,
            type=create_dto.type,
            payload=create_dto.payload,
            created_at=now_tz(),
        )

        await self._activities_repo.add(activity=activity)
