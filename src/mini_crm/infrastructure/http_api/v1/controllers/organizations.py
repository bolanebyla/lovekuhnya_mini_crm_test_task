from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.use_cases import GetUserOrganizationsUseCase
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import UserOrganizationSchema

organizations_v1_router = APIRouter(
    prefix="/organizations",
    route_class=DishkaRoute,
    tags=["Организации"],
)


@organizations_v1_router.get("/me")
async def me(
    use_case: FromDishka[GetUserOrganizationsUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> list[UserOrganizationSchema]:
    """Возвращает список организаций, в которых состоит текущий пользователь"""
    result = await use_case.execute(user_id=current_user.user_id)

    return [UserOrganizationSchema.from_dto(dto=dto) for dto in result]
