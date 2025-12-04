from commons.app_errors.errors import ForbiddenUserActionError
from commons.dtos.pagination import Page
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.deals.dtos import DealShortDto, GetDealsByCriteriaDto
from mini_crm.application.deals.interfaces import DealsReadRepo
from mini_crm.application.organizations.enums import OrganizationMemberRoles


class GetDealsByCriteriaUseCase:
    """Получение списка сделок по критериям"""

    def __init__(
        self,
        operation: AsyncOperation,
        deals_read_repo: DealsReadRepo,
    ):
        self._operation = operation
        self._deals_read_repo = deals_read_repo

        self._allowed_filter_by_owner_id_roles = [
            OrganizationMemberRoles.MANAGER,
            OrganizationMemberRoles.ADMIN,
            OrganizationMemberRoles.OWNER,
        ]

    @async_operation
    async def execute(
        self,
        criteria: GetDealsByCriteriaDto,
    ) -> Page[DealShortDto]:
        if (
            criteria.owner_id is not None
            and criteria.current_user.role not in self._allowed_filter_by_owner_id_roles
        ):
            raise ForbiddenUserActionError(
                user_id=criteria.current_user.user_id,
                role=criteria.current_user.role,
                action="Фильтрация сделок по владельцу",
            )

        return await self._deals_read_repo.get_page_by_criteria(criteria=criteria)
