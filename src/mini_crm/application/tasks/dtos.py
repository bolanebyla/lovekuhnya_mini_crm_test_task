from dataclasses import dataclass
from datetime import date, datetime

from commons.entities import EntityId
from mini_crm.application.organizations.dtos import OrganizationMemberDto


@dataclass(kw_only=True)
class CreateTaskDto:
    """DTO создания задачи"""

    deal_id: EntityId
    title: str
    description: str
    due_date: date


@dataclass(kw_only=True)
class GetTasksByCriteriaDto:
    """Критерии для получения задач"""

    deal_id: EntityId | None = None
    """Фильтр по сделке"""

    only_open: bool = False
    """Только открытые задачи (is_done=false)"""

    due_before: date | None = None
    """Задачи со сроком до указанной даты"""

    due_after: date | None = None
    """Задачи со сроком после указанной даты"""

    current_user: OrganizationMemberDto


@dataclass(kw_only=True)
class TaskShortDto:
    """Краткая информация по задаче"""

    id: EntityId
    deal_id: EntityId
    title: str
    description: str
    due_date: date
    is_done: bool
    created_at: datetime
