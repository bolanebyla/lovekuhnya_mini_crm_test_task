from commons.app_errors.errors import EntityNotFoundByIdError, ForbiddenError
from commons.datetime_utils import now_tz
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.contacts.entities import Contact
from mini_crm.application.contacts.interfaces import ContactsRepo
from mini_crm.application.deals.dtos import CreateDealDto
from mini_crm.application.deals.entities import Deal
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class CreateDealUseCase:
    """Создать сделку"""

    def __init__(
        self,
        operation: AsyncOperation,
        deals_repo: DealsRepo,
        contacts_repo: ContactsRepo,
    ):
        self._operation = operation
        self._deals_repo = deals_repo
        self._contacts_repo = contacts_repo

    @async_operation
    async def execute(
        self,
        create_dto: CreateDealDto,
        current_user: OrganizationMemberDto,
    ) -> None:
        contact = await self._contacts_repo.get_by_id(id_=create_dto.contact_id)
        if contact is None:
            raise EntityNotFoundByIdError(
                entity=Contact.__name__,
                id_=create_dto.contact_id,
            )

        if contact.organization_id != current_user.organization_id:
            raise ForbiddenError()

        now = now_tz()

        deal = Deal(
            contact_id=create_dto.contact_id,
            title=create_dto.title,
            amount=create_dto.amount,
            currency=create_dto.currency,
            organization_id=current_user.organization_id,
            owner_id=current_user.user_id,
            status=DealStatuses.NEW,
            stage=DealStages.QUALIFICATION,
            created_at=now,
            updated_at=now,
        )

        await self._deals_repo.add(deal=deal)
