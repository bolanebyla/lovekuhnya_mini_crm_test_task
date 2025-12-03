from commons.dtos.pagination import Page
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.contacts.dtos import ContactShortDto, GetContactsByCriteriaDto
from mini_crm.application.contacts.interfaces import ContactsReadRepo


class GetContactsByCriteriaUseCase:
    """Возвращает список контактов по критериям"""

    def __init__(
        self,
        operation: AsyncOperation,
        contacts_read_repo: ContactsReadRepo,
    ):
        self._operation = operation
        self._contacts_read_repo = contacts_read_repo

    @async_operation
    async def execute(
        self,
        criteria: GetContactsByCriteriaDto,
    ) -> Page[ContactShortDto]:
        # TODO: проверять роли пользователя и устанавливать owner_id

        contacts_page = await self._contacts_read_repo.get_page_by_criteria(criteria=criteria)
        return contacts_page
