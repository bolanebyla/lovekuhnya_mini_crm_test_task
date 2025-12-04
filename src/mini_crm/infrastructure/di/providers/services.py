from dishka import Provider, Scope, provide

from mini_crm.application.deals.services import DealsService


class ServicesProvider(Provider):
    scope = Scope.REQUEST

    deals_service = provide(DealsService)
