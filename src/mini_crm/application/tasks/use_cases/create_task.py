from datetime import date

from commons.app_errors.errors import ForbiddenError
from commons.datetime_utils import now_tz
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.deals.entities import Deal
from mini_crm.application.deals.services import DealsService
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.tasks.dtos import CreateTaskDto
from mini_crm.application.tasks.entities import Task
from mini_crm.application.tasks.errors import TaskDueDateInPastError
from mini_crm.application.tasks.interfaces import TasksRepo


class CreateTaskUseCase:
    """Создать задачу"""

    _allowed_roles_for_any_deal = (
        OrganizationMemberRoles.OWNER,
        OrganizationMemberRoles.ADMIN,
        OrganizationMemberRoles.MANAGER,
    )
    """Роли, которым разрешено создавать задачи для любой сделки в организации"""

    def __init__(
        self,
        operation: AsyncOperation,
        tasks_repo: TasksRepo,
        deals_service: DealsService,
    ):
        self._operation = operation
        self._tasks_repo = tasks_repo
        self._deals_service = deals_service

    @async_operation
    async def execute(
        self,
        create_dto: CreateTaskDto,
        current_user: OrganizationMemberDto,
    ) -> None:
        self._validate_due_date(due_date=create_dto.due_date)

        deal = await self._deals_service.get_deal_for_user(
            deal_id=create_dto.deal_id,
            current_user=current_user,
        )

        self._validate_user_rights_to_add_tasks_to_deal(
            deal=deal,
            current_user=current_user,
        )

        task = Task(
            deal_id=create_dto.deal_id,
            title=create_dto.title,
            description=create_dto.description,
            due_date=create_dto.due_date,
            is_done=False,
            created_at=now_tz(),
        )

        await self._tasks_repo.add(task=task)

    def _validate_due_date(self, due_date: date) -> None:
        """Проверяет, что due_date не в прошлом (минимум сегодня)"""
        today = now_tz().date()
        if due_date < today:
            raise TaskDueDateInPastError()

    def _validate_user_rights_to_add_tasks_to_deal(
        self,
        deal: Deal,
        current_user: OrganizationMemberDto,
    ) -> None:
        """Проверяет, что у пользователя есть права на добавление задач к сделке"""
        if (
            current_user.role not in self._allowed_roles_for_any_deal
            and deal.owner_id != current_user.user_id
        ):
            raise ForbiddenError()
