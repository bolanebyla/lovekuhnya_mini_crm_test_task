from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Protocol

from commons.entities import EntityId
from mini_crm.application.deals.dtos import DealStatusSummaryDto


class DealsAnalyticsRepo(Protocol):
    """Репозиторий для аналитики по сделкам"""

    @abstractmethod
    async def get_summary_by_status(
        self,
        organization_id: EntityId,
    ) -> list[DealStatusSummaryDto]:
        """Получает количество и сумму сделок по статусам"""
        ...

    @abstractmethod
    async def get_won_average_amount(
        self,
        organization_id: EntityId,
    ) -> Decimal | None:
        """Получает средний amount по выигранным сделкам"""
        ...

    @abstractmethod
    async def get_new_deals_count(
        self,
        organization_id: EntityId,
        since: datetime,
    ) -> int:
        """Получает количество новых сделок с указанной даты"""
        ...
