from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from commons.dtos.pagination import PaginatedRequestDto
from commons.entities import EntityId
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class DealOrderBy(StrEnum):
    """Поля для сортировки сделок"""

    CREATED_AT = "created_at"
    AMOUNT = "amount"
    UPDATED_AT = "updated_at"


class OrderDirection(StrEnum):
    """Направление сортировки"""

    ASC = "asc"
    DESC = "desc"


@dataclass(kw_only=True)
class GetDealsByCriteriaDto(PaginatedRequestDto):
    """Критерии для получения сделок"""

    current_user: OrganizationMemberDto

    statuses: list[DealStatuses] | None = None
    stage: DealStages | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None
    owner_id: EntityId | None = None

    order_by: DealOrderBy = DealOrderBy.CREATED_AT
    order: OrderDirection = OrderDirection.DESC


@dataclass(kw_only=True)
class DealShortDto:
    """Краткая информация по сделке"""

    id: EntityId
    contact_id: EntityId
    owner_id: EntityId
    title: str
    amount: Decimal
    currency: str
    status: DealStatuses
    stage: DealStages
    created_at: datetime
    updated_at: datetime


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
