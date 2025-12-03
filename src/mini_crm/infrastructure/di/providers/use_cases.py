from dishka import Provider, Scope, provide

from mini_crm.application.contacts.use_cases import GetContactsByCriteriaUseCase
from mini_crm.application.organizations.use_cases import GetUserOrganisationsUseCase


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_user_organisations = provide(GetUserOrganisationsUseCase)
    get_contacts_by_criteria = provide(GetContactsByCriteriaUseCase)
