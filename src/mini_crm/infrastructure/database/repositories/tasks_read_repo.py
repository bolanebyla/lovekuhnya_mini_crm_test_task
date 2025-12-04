from sqlalchemy import select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from mini_crm.application.tasks.dtos import GetTasksByCriteriaDto, TaskShortDto
from mini_crm.application.tasks.interfaces import TasksReadRepo
from mini_crm.infrastructure.database.tables import deals_table, tasks_table


class TasksReadRepoImpl(BaseReadOnlyRepository, TasksReadRepo):
    async def get_by_criteria(
        self,
        criteria: GetTasksByCriteriaDto,
    ) -> list[TaskShortDto]:
        filters = [
            deals_table.c.organization_id == criteria.current_user.organization_id,
        ]

        if criteria.deal_id is not None:
            filters.append(tasks_table.c.deal_id == criteria.deal_id)

        if criteria.only_open:
            filters.append(tasks_table.c.is_done.is_(False))

        if criteria.due_before is not None:
            filters.append(tasks_table.c.due_date <= criteria.due_before)

        if criteria.due_after is not None:
            filters.append(tasks_table.c.due_date >= criteria.due_after)

        query = (
            select(
                tasks_table.c.id,
                tasks_table.c.deal_id,
                tasks_table.c.title,
                tasks_table.c.description,
                tasks_table.c.due_date,
                tasks_table.c.is_done,
                tasks_table.c.created_at,
            )
            .select_from(tasks_table.join(deals_table, tasks_table.c.deal_id == deals_table.c.id))
            .where(*filters)
        )

        db_items = (await self.session.execute(query)).mappings().all()

        return [
            TaskShortDto(
                id=db_item.id,
                deal_id=db_item.deal_id,
                title=db_item.title,
                description=db_item.description,
                due_date=db_item.due_date,
                is_done=db_item.is_done,
                created_at=db_item.created_at,
            )
            for db_item in db_items
        ]
