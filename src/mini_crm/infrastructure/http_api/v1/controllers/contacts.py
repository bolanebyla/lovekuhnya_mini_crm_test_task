from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends, Query

from commons.http_api.schemas import PageSchema
from mini_crm.application.contacts.use_cases import (
    CreateContactUseCase,
    GetContactsByCriteriaUseCase,
)
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import (
    ContactShortSchema,
    CreateContactSchema,
    GetContactsByCriteriaSchema,
)

contacts_v1_router = APIRouter(
    prefix="/contacts",
    route_class=DishkaRoute,
    tags=["Контакты"],
)


@contacts_v1_router.get("/")
async def get_list_by_criteria(
    criteria_schema: Annotated[GetContactsByCriteriaSchema, Query()],
    use_case: FromDishka[GetContactsByCriteriaUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> PageSchema[ContactShortSchema]:
    """Возвращает список контактов по критериям"""
    criteria = criteria_schema.to_dto(current_user=current_user)

    result = await use_case.execute(criteria=criteria)

    return PageSchema(
        items=[ContactShortSchema.from_dto(dto=dto) for dto in result.items],
        page=result.page,
        page_size=result.page_size,
        total=result.total,
        pages=result.pages,
    )


@contacts_v1_router.post("/")
async def create_contact(
    create_schema: Annotated[CreateContactSchema, Body()],
    use_case: FromDishka[CreateContactUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> None:
    """Создание контакта"""
    create_dto = create_schema.to_dto()

    await use_case.execute(
        create_dto=create_dto,
        current_user=current_user,
    )
