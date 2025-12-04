from pydantic_settings import BaseSettings


class CacheSettings(BaseSettings):
    CASH_URL: str = "mem://?check_interval=10&size=10000"
    CASH_ENABLED: bool = True
