from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends

from mini_crm.application.deals.use_cases import CreateDealUseCase
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import (
    CreateDealSchema,
)

deals_v1_router = APIRouter(
    prefix="/deals",
    route_class=DishkaRoute,
    tags=["Сделки"],
)


@deals_v1_router.post("/")
async def create_deal(
    create_schema: Annotated[CreateDealSchema, Body()],
    use_case: FromDishka[CreateDealUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> None:
    """Создание контакта"""
    create_dto = create_schema.to_dto()

    await use_case.execute(
        create_dto=create_dto,
        current_user=current_user,
    )
