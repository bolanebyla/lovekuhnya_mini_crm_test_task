from decimal import Decimal

from pydantic import BaseModel, Field

from mini_crm.application.deals.dtos import DealsSummaryDto, DealStatusSummaryDto
from mini_crm.application.deals.enums import DealStatuses


class GetDealsSummaryQuerySchema(BaseModel):
    """Параметры запроса сводки по сделкам"""

    new_deals_days: int = Field(default=30, description="Период для новых сделок (дней)")


class DealStatusSummarySchema(BaseModel):
    """Сводка по статусу сделки"""

    status: DealStatuses
    count: int
    total_amount: Decimal

    @classmethod
    def from_dto(cls, dto: DealStatusSummaryDto) -> "DealStatusSummarySchema":
        return cls(
            status=dto.status,
            count=dto.count,
            total_amount=dto.total_amount,
        )


class DealsSummarySchema(BaseModel):
    """Сводка по сделкам"""

    by_status: list[DealStatusSummarySchema]
    won_average_amount: Decimal | None = None
    new_deals_count: int

    @classmethod
    def from_dto(cls, dto: DealsSummaryDto) -> "DealsSummarySchema":
        return cls(
            by_status=[DealStatusSummarySchema.from_dto(s) for s in dto.by_status],
            won_average_amount=dto.won_average_amount,
            new_deals_count=dto.new_deals_count,
        )
