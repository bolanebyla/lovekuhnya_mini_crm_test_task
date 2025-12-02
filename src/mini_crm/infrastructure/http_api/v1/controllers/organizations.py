from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from mini_crm.application.organizations.use_cases import GetUserOrganisations
from mini_crm.infrastructure.http_api.auth import CurrentUser, get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import UserOrganisationSchema

organizations_v1_router = APIRouter(
    prefix="/organizations",
    route_class=DishkaRoute,
    tags=["Организации"],
)


@organizations_v1_router.get("/me")
async def get_list_by_criteria(
    use_case: FromDishka[GetUserOrganisations],
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> list[UserOrganisationSchema]:
    """Возвращает список организаций, в которых состоит текущий пользователь"""
    result = await use_case.execute(user_id=current_user.user_id)

    return [UserOrganisationSchema.from_dto(dto=dto) for dto in result]
