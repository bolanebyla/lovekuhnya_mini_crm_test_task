import sys

from alembic.config import CommandLine, Config

from mini_crm.infrastructure import log
from mini_crm.infrastructure.database.settings import AlembicSettings, DBSettings

db_settings = DBSettings()
alembic_settings = AlembicSettings()


log.configure(db_settings.LOGGING_CONFIG)


def make_config() -> Config:
    """
    Создаёт конфиг для логера
    """
    config = Config()
    config.set_main_option("script_location", alembic_settings.ALEMBIC_SCRIPT_LOCATION)
    config.set_main_option("version_locations", alembic_settings.ALEMBIC_VERSION_LOCATIONS)
    config.set_main_option("sqlalchemy.url", db_settings.DB_URL)
    config.set_main_option(
        "file_template",
        alembic_settings.ALEMBIC_MIGRATION_FILENAME_TEMPLATE,
    )
    config.set_main_option("timezone", "UTC")

    return config


def run_cmd(*args: str) -> None:
    log.configure(db_settings.LOGGING_CONFIG)
    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))


if __name__ == "__main__":
    run_cmd(*sys.argv[1:])
