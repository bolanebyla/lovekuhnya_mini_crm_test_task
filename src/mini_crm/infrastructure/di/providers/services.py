from dishka import Provider, Scope, provide

from mini_crm.application.activities.services import ActivitiesService
from mini_crm.application.deals.services import DealsService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    activities_service = provide(ActivitiesService)
    deals_service = provide(DealsService)
