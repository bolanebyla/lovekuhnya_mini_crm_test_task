from typing import Any

from pydantic_settings import BaseSettings


class HttpApiSettings(BaseSettings):
    LOGGING_LEVEL: str = "INFO"
    HTTP_API_DEBUG_MODE: bool = False

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: str = "*"
    CORS_ALLOW_HEADERS: str = "*"

    @property
    def LOGGING_CONFIG(self) -> dict[str, Any]:
        config = {
            "loggers": {
                "uvicorn": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "uvicorn.access": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "uvicorn.error": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "uvicorn.asgi": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "gunicorn": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "gunicorn.access": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
                "gunicorn.error": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                },
            }
        }

        return config

    def get_formated_cors_allow_origins(self) -> list[str]:
        return self.CORS_ALLOW_ORIGINS.split(",")

    def get_formated_cors_allow_methods(self) -> list[str]:
        return self.CORS_ALLOW_METHODS.split(",")

    def get_formated_cors_allow_headers(self) -> list[str]:
        return self.CORS_ALLOW_HEADERS.split(",")


class ApiSecuritySettings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int | float = 10
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int | float = 60 * 24 * 30  # 1 месяц
    JWT_BEELINE_MOBILE_ID_NOTIFICATION_TOKEN_EXPIRE_MINUTES: int | float = 10


class HttpApiPrometheusMetricsSettings(BaseSettings):
    PROMETHEUS_METRICS_ENABLED: bool = True
    PROMETHEUS_METRICS_ENDPOINT: str = "/metrics"
