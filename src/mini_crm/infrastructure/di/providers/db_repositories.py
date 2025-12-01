from dishka import Provider, Scope, provide

from mini_crm.application.organizations.interfaces import OrganizationsReadRepo
from mini_crm.infrastructure.database.repositories import OrganizationsReadRepoImpl


class DBRepositoriesProvider(Provider):
    scope = Scope.REQUEST

    organizations_read_repo = provide(OrganizationsReadRepoImpl, provides=OrganizationsReadRepo)
