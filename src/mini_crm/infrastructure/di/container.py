from dishka import AsyncContainer, make_async_container

from mini_crm.infrastructure.database.settings import DBSettings
from mini_crm.infrastructure.http_api.settings import (
    HttpApiPrometheusMetricsSettings,
    HttpApiSettings,
)

from .providers import (
    DBProvider,
    DBRepositoriesProvider,
    OperationsProvider,
    ServicesProvider,
    UseCasesProvider,
)


def create_http_api_container(
    api_settings: HttpApiSettings,
    api_prometheus_metrics_settings: HttpApiPrometheusMetricsSettings,
    db_settings: DBSettings,
) -> AsyncContainer:
    container = make_async_container(
        UseCasesProvider(),
        OperationsProvider(),
        DBRepositoriesProvider(),
        ServicesProvider(),
        DBProvider(),
        context={
            HttpApiSettings: api_settings,
            HttpApiPrometheusMetricsSettings: api_prometheus_metrics_settings,
            DBSettings: db_settings,
        },
    )
    return container
