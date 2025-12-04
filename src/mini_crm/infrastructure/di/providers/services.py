from dishka import Provider, Scope, provide

from mini_crm.application.activities.services import ActivitiesService
from mini_crm.application.deals.services import DealsService
from mini_crm.application.organizations.services import (
    OrganizationMembersService,
    OrganizationsService,
)


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    activities_service = provide(ActivitiesService)
    deals_service = provide(DealsService)
    organization_members_service = provide(OrganizationMembersService)
    organizations_service = provide(OrganizationsService)
