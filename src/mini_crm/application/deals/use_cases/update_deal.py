from commons.operations import AsyncOperation, async_operation
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
    ):
        self._operation = operation
        self._deals_repo = deals_repo
        self._deals_service = deals_service

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

        deal.set_status(status=update_dto.status)

        skip_stage_order_validation = (
            current_user.role in self._allowed_roles_to_roll_back_deal_stage
        )
        deal.set_stage(
            stage=update_dto.stage,
            skip_order_validation=skip_stage_order_validation,
        )

        # TODO: создавать Activity

        await self._deals_repo.add(deal=deal)
