from datetime import date

from mini_crm.application.tasks.dtos import CreateTaskDto


def create_task_dto(
    deal_id: int = 1,
    title: str = "Test Task",
    description: str = "Test Description",
    due_date: date | None = None,
) -> CreateTaskDto:
    return CreateTaskDto(
        deal_id=deal_id,
        title=title,
        description=description,
        due_date=due_date or date.today(),
    )
