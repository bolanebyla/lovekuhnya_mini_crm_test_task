from commons.app_errors.errors import EntityNotFoundByIdError, ForbiddenError
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.deals.dtos import UpdateDealDto
from mini_crm.application.deals.entities import Deal
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.enums import OrganizationMemberRoles


class UpdateDealUseCase:
    """Обновить сделку"""

    def __init__(
        self,
        operation: AsyncOperation,
        deals_repo: DealsRepo,
    ):
        self._operation = operation
        self._deals_repo = deals_repo

        self._allowed_roles_to_roll_back_deal_stage = (
            OrganizationMemberRoles.ADMIN,
            OrganizationMemberRoles.OWNER,
        )

    @async_operation
    async def execute(
        self,
        update_dto: UpdateDealDto,
        current_user: OrganizationMemberDto,
    ) -> None:
        deal = await self._deals_repo.get_by_id(id_=update_dto.deal_id)
        if deal is None:
            raise EntityNotFoundByIdError(
                entity=Deal.__name__,
                id_=update_dto.deal_id,
            )

        if deal.organization_id != current_user.organization_id:
            raise ForbiddenError()

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
