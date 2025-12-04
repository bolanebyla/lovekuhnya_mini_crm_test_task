from enum import StrEnum


class ActivityTypes(StrEnum):
    """Типы активностей по сделке"""

    COMMENT = "comment"
    """Комментарий"""

    STATUS_CHANGED = "status_changed"
    """Изменение статуса сделки"""

    STAGE_CHANGED = "stage_changed"
    """Изменение стадии сделки"""

    TASK_CREATED = "task_created"
    """Создание задачи"""

    SYSTEM = "system"
    """Системное событие"""
