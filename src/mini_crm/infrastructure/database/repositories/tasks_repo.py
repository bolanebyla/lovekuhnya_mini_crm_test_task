from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.tasks.entities import Task
from mini_crm.application.tasks.interfaces import TasksRepo


class TasksRepoImpl(BaseRepository, TasksRepo):
    async def add(self, task: Task) -> None:
        self.session.add(task)
        await self.session.flush()
