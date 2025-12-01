from dishka import Provider, Scope, provide

from mini_crm.application.organizations.use_cases import GetUserOrganisations


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_user_organisations = provide(GetUserOrganisations)
