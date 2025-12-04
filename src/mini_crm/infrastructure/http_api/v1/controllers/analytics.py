from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from mini_crm.application.deals.use_cases import GetDealsFunnelUseCase, GetDealsSummaryUseCase
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1.schemas import (
    DealsFunnelSchema,
    DealsSummarySchema,
)

analytics_v1_router = APIRouter(
    prefix="/analytics",
    route_class=DishkaRoute,
    tags=["Аналитика"],
)


@analytics_v1_router.get("/deals/summary")
async def get_deals_summary(
    use_case: FromDishka[GetDealsSummaryUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> DealsSummarySchema:
    """Сводка по сделкам для текущей организации"""
    result = await use_case.execute(
        current_user=current_user,
    )

    return DealsSummarySchema.from_dto(dto=result)


@analytics_v1_router.get("/deals/funnel")
async def get_deals_funnel(
    use_case: FromDishka[GetDealsFunnelUseCase],
    current_user: Annotated[OrganizationMemberDto, Depends(get_current_user)],
) -> DealsFunnelSchema:
    """Воронка продаж для текущей организации"""
    result = await use_case.execute(current_user=current_user)
    return DealsFunnelSchema.from_dto(dto=result)
