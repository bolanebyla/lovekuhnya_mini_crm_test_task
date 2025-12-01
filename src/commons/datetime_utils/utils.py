from datetime import UTC, datetime


def now_tz() -> datetime:
    """
    Получение текущего времени с часовым поясом
    """
    return datetime.now(UTC)
