from typing import cast

from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.activities.services import ActivitiesService
from mini_crm.application.deals.dtos import UpdateDealDto
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.deals.services import DealsService
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.enums import OrganizationMemberRoles


class UpdateDealUseCase:
    """Обновить сделку"""

    _allowed_roles_to_roll_back_deal_stage = (
        OrganizationMemberRoles.ADMIN,
        OrganizationMemberRoles.OWNER,
    )

    def __init__(
        self,
        operation: AsyncOperation,
        deals_repo: DealsRepo,
        deals_service: DealsService,
        activities_service: ActivitiesService,
    ):
        self._operation = operation
        self._deals_repo = deals_repo
        self._deals_service = deals_service
        self._activities_service = activities_service

    @async_operation
    async def execute(
        self,
        update_dto: UpdateDealDto,
        current_user: OrganizationMemberDto,
    ) -> None:
        deal = await self._deals_service.get_deal_for_user(
            deal_id=update_dto.deal_id,
            current_user=current_user,
        )

        old_status = deal.status
        old_stage = deal.stage

        deal.set_status(status=update_dto.status)

        skip_stage_order_validation = (
            current_user.role in self._allowed_roles_to_roll_back_deal_stage
        )
        deal.set_stage(
            stage=update_dto.stage,
            skip_order_validation=skip_stage_order_validation,
        )

        await self._deals_repo.add(deal=deal)

        # Создаём активности при изменении статуса/стадии
        if old_status != deal.status:
            await self._activities_service.create_status_changed_activity(
                deal_id=cast(EntityId, deal.id),
                old_status=old_status,
                new_status=deal.status,
            )

        if old_stage != deal.stage:
            await self._activities_service.create_stage_changed_activity(
                deal_id=cast(EntityId, deal.id),
                old_stage=old_stage,
                new_stage=deal.stage,
            )
