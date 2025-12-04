from abc import abstractmethod
from typing import Protocol

from mini_crm.application.tasks.entities import Task


class TasksRepo(Protocol):
    """Репозиторий для задач"""

    @abstractmethod
    async def add(self, task: Task) -> None:
        """Добавляет задачу в хранилище"""
        ...
