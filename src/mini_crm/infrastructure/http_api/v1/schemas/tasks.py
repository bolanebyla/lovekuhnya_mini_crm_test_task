from datetime import date, datetime

from pydantic import BaseModel, Field

from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.tasks.dtos import CreateTaskDto, GetTasksByCriteriaDto, TaskShortDto


class CreateTaskSchema(BaseModel):
    """Схема создания задачи"""

    deal_id: int = Field(..., description="ID сделки")
    title: str = Field(..., description="Заголовок задачи")
    description: str = Field(..., description="Описание задачи")
    due_date: date = Field(..., description="Срок выполнения")

    def to_dto(self) -> CreateTaskDto:
        return CreateTaskDto(
            deal_id=self.deal_id,
            title=self.title,
            description=self.description,
            due_date=self.due_date,
        )


class GetTasksByCriteriaSchema(BaseModel):
    """Схема критериев для получения списка задач"""

    deal_id: int | None = Field(None, description="Фильтр по сделке")
    only_open: bool = Field(False, description="Только открытые задачи (is_done=false)")
    due_before: date | None = Field(None, description="Задачи со сроком до указанной даты")
    due_after: date | None = Field(None, description="Задачи со сроком после указанной даты")

    def to_dto(self, current_user: OrganizationMemberDto) -> GetTasksByCriteriaDto:
        return GetTasksByCriteriaDto(
            deal_id=self.deal_id,
            only_open=self.only_open,
            due_before=self.due_before,
            due_after=self.due_after,
            current_user=current_user,
        )


class TaskShortSchema(BaseModel):
    """Краткая информация по задаче"""

    id: int
    deal_id: int
    title: str
    description: str
    due_date: date
    is_done: bool
    created_at: datetime

    @classmethod
    def from_dto(cls, dto: TaskShortDto) -> "TaskShortSchema":
        return cls(
            id=dto.id,
            deal_id=dto.deal_id,
            title=dto.title,
            description=dto.description,
            due_date=dto.due_date,
            is_done=dto.is_done,
            created_at=dto.created_at,
        )
