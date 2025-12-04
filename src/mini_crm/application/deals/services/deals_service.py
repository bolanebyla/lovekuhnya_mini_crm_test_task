from commons.app_errors.errors import EntityNotFoundByIdError, ForbiddenError
from commons.entities import EntityId
from mini_crm.application.deals.entities import Deal
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class DealsService:
    """Сервис для работы со сделками"""

    def __init__(self, deals_repo: DealsRepo):
        self._deals_repo = deals_repo

    async def get_deal_for_user(
        self,
        deal_id: EntityId,
        current_user: OrganizationMemberDto,
    ) -> Deal:
        """Получает сделку по ID и проверяет, что она принадлежит организации пользователя"""
        deal = await self._deals_repo.get_by_id(id_=deal_id)
        if deal is None:
            raise EntityNotFoundByIdError(
                entity=Deal.__name__,
                id_=deal_id,
            )

        if deal.organization_id != current_user.organization_id:
            raise ForbiddenError()

        return deal
