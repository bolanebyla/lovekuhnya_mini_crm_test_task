from decimal import Decimal

from pydantic import BaseModel

from mini_crm.application.deals.dtos import (
    DealsFunnelDto,
    DealsSummaryDto,
    DealStageConversionDto,
    DealStageFunnelItemDto,
    DealStatusSummaryDto,
)
from mini_crm.application.deals.enums import DealStages, DealStatuses


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


class DealStageFunnelItemSchema(BaseModel):
    """Элемент воронки: количество сделок по стадии и статусу"""

    stage: DealStages
    status: DealStatuses
    count: int

    @classmethod
    def from_dto(cls, dto: DealStageFunnelItemDto) -> "DealStageFunnelItemSchema":
        return cls(
            stage=dto.stage,
            status=dto.status,
            count=dto.count,
        )


class DealStageConversionSchema(BaseModel):
    """Конверсия между стадиями"""

    from_stage: DealStages
    to_stage: DealStages
    conversion_percent: Decimal

    @classmethod
    def from_dto(cls, dto: DealStageConversionDto) -> "DealStageConversionSchema":
        return cls(
            from_stage=dto.from_stage,
            to_stage=dto.to_stage,
            conversion_percent=dto.conversion_percent,
        )


class DealsFunnelSchema(BaseModel):
    """Воронка продаж"""

    by_stage_and_status: list[DealStageFunnelItemSchema]
    conversions: list[DealStageConversionSchema]

    @classmethod
    def from_dto(cls, dto: DealsFunnelDto) -> "DealsFunnelSchema":
        return cls(
            by_stage_and_status=[
                DealStageFunnelItemSchema.from_dto(item) for item in dto.by_stage_and_status
            ],
            conversions=[DealStageConversionSchema.from_dto(conv) for conv in dto.conversions],
        )
