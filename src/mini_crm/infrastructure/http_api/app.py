import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from commons.app_errors import AppError
from commons.http_api.exception_handlers import app_error_handler, validation_exception_handler
from mini_crm.infrastructure.http_api import (
    HttpApiPrometheusMetricsSettings,
    HttpApiSettings,
)
from mini_crm.infrastructure.http_api.metrics import (
    configure_prometheus_metrics_endpoint,
)
from mini_crm.infrastructure.http_api.v1 import v1_router

root_router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """
    Выполняет действия перед запуском и после завершения основного приложения
    """
    logger = logging.getLogger("FastAPI lifespan")
    logger.info("Загрузка lifespan...")

    logger.info("Lifespan загружен")
    yield
    logger.info("Выполняется очистка lifespan...")

    await app.state.dishka_container.close()
    logger.info("Очистка lifespan завершена")


def create_app(
    api_settings: HttpApiSettings,
    container: AsyncContainer,
    api_prometheus_metrics_settings: HttpApiPrometheusMetricsSettings,
) -> FastAPI:
    """
    Создаёт инстанс fast api
    """
    app = FastAPI(
        title="Mini CRM",
        lifespan=lifespan,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=api_settings.get_formated_cors_allow_origins(),
                allow_credentials=api_settings.CORS_ALLOW_CREDENTIALS,
                allow_methods=api_settings.get_formated_cors_allow_methods(),
                allow_headers=api_settings.get_formated_cors_allow_headers(),
            )
        ],
        debug=api_settings.HTTP_API_DEBUG_MODE,
    )

    app.include_router(root_router)
    api_router = APIRouter(prefix="/api")

    api_router.include_router(v1_router)

    app.include_router(api_router)

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    configure_prometheus_metrics_endpoint(
        app=app,
        settings=api_prometheus_metrics_settings,
    )

    setup_dishka(container=container, app=app)

    return app


@root_router.get("/", include_in_schema=False)
async def docs_redirect() -> RedirectResponse:
    """
    Редирект на страницу документации
    """
    return RedirectResponse(url="/docs")
