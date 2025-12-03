from dishka import Provider, Scope, provide

from mini_crm.application.contacts.use_cases import (
    CreateContactUseCase,
    GetContactsByCriteriaUseCase,
)
from mini_crm.application.organizations.use_cases import (
    GetOrganizationMemberByUserUseCase,
    GetUserOrganizationsUseCase,
)


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_organization_member = provide(GetOrganizationMemberByUserUseCase)
    get_user_organizations = provide(GetUserOrganizationsUseCase)
    get_contacts_by_criteria = provide(GetContactsByCriteriaUseCase)
    create_contact_use_case = provide(CreateContactUseCase)
