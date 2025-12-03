from dishka import Provider, Scope, provide

from mini_crm.application.contacts.interfaces import ContactsReadRepo
from mini_crm.application.organizations.interfaces import (
    OrganizationMembersReadRepo,
    OrganizationsReadRepo,
)
from mini_crm.infrastructure.database.repositories import (
    ContactsReadRepoImpl,
    OrganizationMembersReadRepoImpl,
    OrganizationsReadRepoImpl,
)


class DBRepositoriesProvider(Provider):
    scope = Scope.REQUEST

    organization_members_read_repo = provide(
        OrganizationMembersReadRepoImpl,
        provides=OrganizationMembersReadRepo,
    )
    organizations_read_repo = provide(OrganizationsReadRepoImpl, provides=OrganizationsReadRepo)
    contacts_read_repo = provide(ContactsReadRepoImpl, provides=ContactsReadRepo)
