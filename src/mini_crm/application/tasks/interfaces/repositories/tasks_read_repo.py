from abc import abstractmethod
from typing import Protocol

from mini_crm.application.tasks.dtos import GetTasksByCriteriaDto, TaskShortDto


class TasksReadRepo(Protocol):
    """Репозиторий для чтения задач"""

    @abstractmethod
    async def get_by_criteria(
        self,
        criteria: GetTasksByCriteriaDto,
    ) -> list[TaskShortDto]:
        """Получает список задач по критериям"""
        ...
