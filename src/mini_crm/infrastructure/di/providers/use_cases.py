from dishka import Provider, Scope, provide

from mini_crm.application.activities.use_cases import (
    CreateManualDealActivityUseCase,
    GetActivitiesByDealUseCase,
)
from mini_crm.application.contacts.use_cases import (
    CreateContactUseCase,
    GetContactsByCriteriaUseCase,
)
from mini_crm.application.deals.use_cases import (
    CreateDealUseCase,
    GetDealsFunnelUseCase,
    GetDealsSummaryUseCase,
)
from mini_crm.application.deals.use_cases.update_deal import UpdateDealUseCase
from mini_crm.application.organizations.use_cases import (
    GetOrganizationMemberByUserUseCase,
    GetUserOrganizationsUseCase,
)
from mini_crm.application.tasks.use_cases import CreateTaskUseCase, GetTasksByCriteriaUseCase
from mini_crm.application.users.use_cases import RegisterUserByEmailUseCase


class UseCasesProvider(Provider):
    scope = Scope.REQUEST

    get_organization_member = provide(GetOrganizationMemberByUserUseCase)
    get_user_organizations = provide(GetUserOrganizationsUseCase)
    get_contacts_by_criteria = provide(GetContactsByCriteriaUseCase)
    create_contact = provide(CreateContactUseCase)
    create_deal = provide(CreateDealUseCase)
    update_deal = provide(UpdateDealUseCase)
    get_deals_summary = provide(GetDealsSummaryUseCase)
    get_deals_funnel = provide(GetDealsFunnelUseCase)
    get_tasks_by_criteria = provide(GetTasksByCriteriaUseCase)
    create_task = provide(CreateTaskUseCase)
    get_activities_by_deal = provide(GetActivitiesByDealUseCase)
    create_manual_deal_activity = provide(CreateManualDealActivityUseCase)
    register_user_by_email = provide(RegisterUserByEmailUseCase)
