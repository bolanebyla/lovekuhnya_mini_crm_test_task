from cashews import cache
from cashews.contrib.prometheus import create_metrics_middleware

from .settings import CacheSettings


def setup_cash(cache_settings: CacheSettings) -> None:
    metrics_middleware = create_metrics_middleware()
    cache.setup(
        cache_settings.CASH_URL,
        disable=not cache_settings.CASH_ENABLED,
        middlewares=(metrics_middleware,),
    )
