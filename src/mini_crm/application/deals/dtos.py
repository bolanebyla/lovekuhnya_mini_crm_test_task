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
