import logging

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from mini_crm.infrastructure.http_api.settings import HttpApiPrometheusMetricsSettings


def configure_prometheus_metrics_endpoint(
    app: FastAPI,
    settings: HttpApiPrometheusMetricsSettings,
) -> None:
    """
    Конфигурирует эндпоинт для сбора метрик
    """
    logger = logging.getLogger("configure_metrics_endpoint")

    if settings.PROMETHEUS_METRICS_ENABLED:
        logger.info("Метрики Prometheus включены")
        Instrumentator().instrument(app=app).expose(
            app=app,
            endpoint=settings.PROMETHEUS_METRICS_ENDPOINT,
        )
    else:
        logger.info("Метрики Prometheus выключены")
