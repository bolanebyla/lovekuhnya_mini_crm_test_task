import logging

import uvicorn

from mini_crm.infrastructure import log
from mini_crm.infrastructure.database.settings import DBSettings
from mini_crm.infrastructure.di import create_http_api_container
from mini_crm.infrastructure.http_api.app import create_app
from mini_crm.infrastructure.http_api.settings import (
    ApiSecuritySettings,
    HttpApiPrometheusMetricsSettings,
    HttpApiSettings,
)

api_settings = HttpApiSettings()
api_security_settings = ApiSecuritySettings()
api_prometheus_metrics_settings = HttpApiPrometheusMetricsSettings()
db_settings = DBSettings()


log_config = log.create_config(
    db_settings.LOGGING_CONFIG,
    api_settings.LOGGING_CONFIG,
)
log.configure(
    db_settings.LOGGING_CONFIG,
    api_settings.LOGGING_CONFIG,
)

http_api_container = create_http_api_container(
    api_settings=api_settings,
    api_security_settings=api_security_settings,
    api_prometheus_metrics_settings=api_prometheus_metrics_settings,
    db_settings=db_settings,
)

app = create_app(
    api_settings=api_settings,
    container=http_api_container,
    api_prometheus_metrics_settings=api_prometheus_metrics_settings,
)

if __name__ == "__main__":
    logger = logging.getLogger("UvicornDevServer")
    logger.warning("HTTP API запущено в режиме разработки")

    uvicorn.run(
        "mini_crm.run.http_api:app",
        host="localhost",
        log_level="debug",
        log_config=log_config,
    )
