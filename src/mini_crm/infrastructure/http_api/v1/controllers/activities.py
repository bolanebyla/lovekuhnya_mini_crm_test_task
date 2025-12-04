from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from mini_crm.application.activities.use_cases import GetActivitiesByDealUseCase
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import ActivityShortSchema

activities_v1_router = APIRouter(
    prefix="/deals/{deal_id}/activities",
    route_class=DishkaRoute,
    tags=["Активности"],
)


@activities_v1_router.get("/")
async def get_activities_by_deal(
    deal_id: int,
    use_case: FromDishka[GetActivitiesByDealUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> list[ActivityShortSchema]:
    """Возвращает список активностей по сделке"""
    result = await use_case.execute(
        deal_id=deal_id,
        current_user=current_user,
    )

    return [ActivityShortSchema.from_dto(dto=dto) for dto in result]
