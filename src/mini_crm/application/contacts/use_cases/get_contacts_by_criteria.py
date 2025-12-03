from commons.app_errors.errors import ForbiddenUserActionError
from commons.dtos.pagination import Page
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.contacts.dtos import ContactShortDto, GetContactsByCriteriaDto
from mini_crm.application.contacts.interfaces import ContactsReadRepo
from mini_crm.application.organizations.enums import OrganizationMemberRoles


class GetContactsByCriteriaUseCase:
    """Возвращает список контактов по критериям"""

    def __init__(
        self,
        operation: AsyncOperation,
        contacts_read_repo: ContactsReadRepo,
    ):
        self._operation = operation
        self._contacts_read_repo = contacts_read_repo

        self._allowed_filter_by_owner_id_roles = [
            OrganizationMemberRoles.MANAGER,
            OrganizationMemberRoles.ADMIN,
            OrganizationMemberRoles.OWNER,
        ]

    @async_operation
    async def execute(
        self,
        criteria: GetContactsByCriteriaDto,
    ) -> Page[ContactShortDto]:
        if (
            criteria.owner_id is not None
            and criteria.current_user.role not in self._allowed_filter_by_owner_id_roles
        ):
            raise ForbiddenUserActionError(
                user_id=criteria.current_user.user_id,
                role=criteria.current_user.role,
                action="Фильтрация контактов по владельцу",
            )

        contacts_page = await self._contacts_read_repo.get_page_by_criteria(criteria=criteria)
        return contacts_page
