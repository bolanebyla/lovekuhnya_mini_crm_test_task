from typing import Any

from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_URL: str
    DB_ECHO: bool = False

    LOGGING_LEVEL: str = "INFO"

    @property
    def LOGGING_CONFIG(self) -> dict[str, Any]:
        config = {
            "loggers": {
                "alembic": {
                    "handlers": ["default"],
                    "level": self.LOGGING_LEVEL,
                    "propagate": False,
                }
            }
        }

        if self.DB_ECHO:
            config["loggers"]["sqlalchemy"] = {
                "handlers": ["default"],
                "level": self.LOGGING_LEVEL,
                "propagate": False,
            }

        return config


class AlembicSettings(BaseSettings):
    # Python путь к каталогу, где лежит запускатор alembic
    # (пример: <project_name>.composites:alembic)
    ALEMBIC_SCRIPT_LOCATION: str = "mini_crm.infrastructure.database:alembic"

    # Python путь к каталогу с миграциями
    ALEMBIC_VERSION_LOCATIONS: str = "mini_crm.infrastructure.database:migrations"

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d_%%(minute).2d_%%(second).2d_%%(slug)s"
    )
