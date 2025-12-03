from commons.datetime_utils import now_tz
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.contacts.dtos import CreateContactDto
from mini_crm.application.contacts.entities import Contact
from mini_crm.application.contacts.interfaces import ContactsRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class CreateContactUseCase:
    """Создаёт контакт"""

    def __init__(
        self,
        operation: AsyncOperation,
        contacts_repo: ContactsRepo,
    ):
        self._operation = operation
        self._contacts_repo = contacts_repo

    @async_operation
    async def execute(
        self,
        create_dto: CreateContactDto,
        current_user: OrganizationMemberDto,
    ) -> None:
        contact = Contact(
            name=create_dto.name,
            email=create_dto.email,
            phone=create_dto.phone,
            created_at=now_tz(),
            organization_id=current_user.organization_id,
            owner_id=current_user.user_id,
        )

        await self._contacts_repo.add(contact=contact)
