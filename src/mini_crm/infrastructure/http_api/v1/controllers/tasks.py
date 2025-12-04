from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends, Query

from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.tasks.use_cases import CreateTaskUseCase, GetTasksByCriteriaUseCase
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import (
    CreateTaskSchema,
    GetTasksByCriteriaSchema,
    TaskShortSchema,
)

tasks_v1_router = APIRouter(
    prefix="/tasks",
    route_class=DishkaRoute,
    tags=["Задачи"],
)


@tasks_v1_router.get("/")
async def get_list_by_criteria(
    criteria_schema: Annotated[GetTasksByCriteriaSchema, Query()],
    use_case: FromDishka[GetTasksByCriteriaUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> list[TaskShortSchema]:
    """Возвращает список задач по критериям"""
    criteria = criteria_schema.to_dto(current_user=current_user)

    result = await use_case.execute(criteria=criteria)

    return [TaskShortSchema.from_dto(dto=dto) for dto in result]


@tasks_v1_router.post("/")
async def create_task(
    create_schema: Annotated[CreateTaskSchema, Body()],
    use_case: FromDishka[CreateTaskUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> None:
    """Создание задачи"""
    create_dto = create_schema.to_dto()

    await use_case.execute(
        create_dto=create_dto,
        current_user=current_user,
    )
