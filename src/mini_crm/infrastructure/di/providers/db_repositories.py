from dishka import Provider, Scope, provide

from mini_crm.application.activities.interfaces import ActivitiesRepo
from mini_crm.application.contacts.interfaces import ContactsReadRepo, ContactsRepo
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.organizations.interfaces import (
    OrganizationMembersReadRepo,
    OrganizationsReadRepo,
)
from mini_crm.application.tasks.interfaces import TasksRepo
from mini_crm.infrastructure.database.repositories import (
    ActivitiesRepoImpl,
    ContactsReadRepoImpl,
    ContactsRepoImpl,
    DealsRepoImpl,
    OrganizationMembersReadRepoImpl,
    OrganizationsReadRepoImpl,
    TasksRepoImpl,
)


class DBRepositoriesProvider(Provider):
    scope = Scope.REQUEST

    organization_members_read_repo = provide(
        OrganizationMembersReadRepoImpl,
        provides=OrganizationMembersReadRepo,
    )
    organizations_read_repo = provide(OrganizationsReadRepoImpl, provides=OrganizationsReadRepo)
    contacts_read_repo = provide(ContactsReadRepoImpl, provides=ContactsReadRepo)
    contacts_repo = provide(ContactsRepoImpl, provides=ContactsRepo)
    deals_repo = provide(DealsRepoImpl, provides=DealsRepo)
    tasks_repo = provide(TasksRepoImpl, provides=TasksRepo)
    activities_repo = provide(ActivitiesRepoImpl, provides=ActivitiesRepo)
