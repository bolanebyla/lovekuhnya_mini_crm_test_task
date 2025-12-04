from dishka import Provider, Scope, provide

from mini_crm.application.activities.interfaces import ActivitiesReadRepo, ActivitiesRepo
from mini_crm.application.contacts.interfaces import ContactsReadRepo, ContactsRepo
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.organizations.interfaces import (
    OrganizationMembersReadRepo,
    OrganizationMembersRepo,
    OrganizationsReadRepo,
    OrganizationsRepo,
)
from mini_crm.application.tasks.interfaces import TasksReadRepo, TasksRepo
from mini_crm.application.users.interfaces import UsersRepo
from mini_crm.infrastructure.database.repositories import (
    ActivitiesReadRepoImpl,
    ActivitiesRepoImpl,
    ContactsReadRepoImpl,
    ContactsRepoImpl,
    DealsRepoImpl,
    OrganizationMembersReadRepoImpl,
    OrganizationMembersRepoImpl,
    OrganizationsReadRepoImpl,
    OrganizationsRepoImpl,
    TasksReadRepoImpl,
    TasksRepoImpl,
    UsersRepoImpl,
)


class DBRepositoriesProvider(Provider):
    scope = Scope.REQUEST

    organization_members_read_repo = provide(
        OrganizationMembersReadRepoImpl,
        provides=OrganizationMembersReadRepo,
    )
    organization_members_repo = provide(
        OrganizationMembersRepoImpl,
        provides=OrganizationMembersRepo,
    )
    organizations_read_repo = provide(OrganizationsReadRepoImpl, provides=OrganizationsReadRepo)
    organizations_repo = provide(OrganizationsRepoImpl, provides=OrganizationsRepo)
    contacts_read_repo = provide(ContactsReadRepoImpl, provides=ContactsReadRepo)
    contacts_repo = provide(ContactsRepoImpl, provides=ContactsRepo)
    deals_repo = provide(DealsRepoImpl, provides=DealsRepo)
    tasks_read_repo = provide(TasksReadRepoImpl, provides=TasksReadRepo)
    tasks_repo = provide(TasksRepoImpl, provides=TasksRepo)
    activities_read_repo = provide(ActivitiesReadRepoImpl, provides=ActivitiesReadRepo)
    activities_repo = provide(ActivitiesRepoImpl, provides=ActivitiesRepo)
    users_repo = provide(UsersRepoImpl, provides=UsersRepo)
