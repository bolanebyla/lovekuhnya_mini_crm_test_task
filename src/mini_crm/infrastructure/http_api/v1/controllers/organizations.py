from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from mini_crm.application.organizations.use_cases import GetUserOrganisations
from mini_crm.infrastructure.http_api.v1.schemas import UserOrganisationSchema

organizations_v1_router = APIRouter(
    prefix="/organizations",
    route_class=DishkaRoute,
    tags=["Организации"],
)


@organizations_v1_router.get("/me")
async def get_list_by_criteria(
    use_case: FromDishka[GetUserOrganisations],
) -> list[UserOrganisationSchema]:
    """Возвращает список организаций, в которых состоит текущий пользователь"""

    # TODO: получать id пользователя
    user_id = 1

    result = await use_case.execute(user_id=user_id)

    return [UserOrganisationSchema.from_dto(dto=dto) for dto in result]
