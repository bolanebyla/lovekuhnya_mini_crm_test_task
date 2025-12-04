from commons.operations import AsyncOperation, async_operation
from mini_crm.application.tasks.dtos import GetTasksByCriteriaDto, TaskShortDto
from mini_crm.application.tasks.interfaces import TasksReadRepo


class GetTasksByCriteriaUseCase:
    """Возвращает список задач по критериям"""

    def __init__(
        self,
        operation: AsyncOperation,
        tasks_read_repo: TasksReadRepo,
    ):
        self._operation = operation
        self._tasks_read_repo = tasks_read_repo

    @async_operation
    async def execute(
        self,
        criteria: GetTasksByCriteriaDto,
    ) -> list[TaskShortDto]:
        return await self._tasks_read_repo.get_by_criteria(criteria=criteria)
