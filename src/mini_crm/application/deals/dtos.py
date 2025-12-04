from dataclasses import dataclass
from decimal import Decimal

from commons.entities import EntityId
from mini_crm.application.deals.enums import DealStages, DealStatuses


@dataclass(kw_only=True)
class CreateDealDto:
    """Dto для создания сделки"""

    contact_id: EntityId
    title: str
    amount: Decimal
    currency: str


@dataclass(kw_only=True)
class UpdateDealDto:
    """Dto для обновления сделки"""

    deal_id: EntityId
    status: DealStatuses
    stage: DealStages


@dataclass(kw_only=True)
class DealStatusSummaryDto:
    """Сводка по статусу сделки"""

    status: DealStatuses
    count: int
    total_amount: Decimal


@dataclass(kw_only=True)
class DealsSummaryDto:
    """Сводка по сделкам"""

    by_status: list[DealStatusSummaryDto]
    """Количество и сумма по статусам"""

    won_average_amount: Decimal | None = None
    """Средний amount по выигранным сделкам"""

    new_deals_count: int
    """Количество новых сделок за период"""


@dataclass(kw_only=True)
class DealStageFunnelItemDto:
    """Элемент воронки: количество сделок по стадии и статусу"""

    stage: DealStages
    status: DealStatuses
    count: int


@dataclass(kw_only=True)
class DealStageConversionDto:
    """Конверсия между стадиями"""

    from_stage: DealStages
    to_stage: DealStages
    conversion_percent: Decimal


@dataclass(kw_only=True)
class DealsFunnelDto:
    """Воронка продаж"""

    by_stage_and_status: list[DealStageFunnelItemDto]
    """Количество сделок по стадиям в разрезе статусов"""

    conversions: list[DealStageConversionDto]
    """Конверсия из предыдущей стадии в следующую"""
