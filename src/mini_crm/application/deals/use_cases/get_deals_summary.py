from datetime import timedelta
from decimal import Decimal

from commons.datetime_utils import now_tz
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.deals.dtos import DealsSummaryDto, DealStatusSummaryDto
from mini_crm.application.deals.enums import DealStatuses
from mini_crm.application.deals.interfaces import DealsAnalyticsRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class GetDealsSummaryUseCase:
    """Получить сводку по сделкам"""

    _new_deals_days: int = 30
    """Период для новых сделок (дней)"""

    def __init__(
        self,
        operation: AsyncOperation,
        deals_analytics_repo: DealsAnalyticsRepo,
    ):
        self._operation = operation
        self._deals_analytics_repo = deals_analytics_repo

    @async_operation
    async def execute(
        self,
        current_user: OrganizationMemberDto,
    ) -> DealsSummaryDto:
        organization_id = current_user.organization_id

        by_status = await self._deals_analytics_repo.get_summary_by_status(
            organization_id=organization_id,
        )

        by_status = self._fill_all_statuses(by_status=by_status)

        won_average_amount = await self._deals_analytics_repo.get_won_average_amount(
            organization_id=organization_id,
        )

        since = now_tz() - timedelta(days=self._new_deals_days)
        new_deals_count = await self._deals_analytics_repo.get_new_deals_count(
            organization_id=organization_id,
            since=since,
        )

        return DealsSummaryDto(
            by_status=by_status,
            won_average_amount=won_average_amount,
            new_deals_count=new_deals_count,
        )

    def _fill_all_statuses(
        self,
        by_status: list[DealStatusSummaryDto],
    ) -> list[DealStatusSummaryDto]:
        """Заполняет статистику по всем статусам, даже если данных нет"""
        status_map = {item.status: item for item in by_status}

        return [
            status_map.get(
                status,
                DealStatusSummaryDto(
                    status=status,
                    count=0,
                    total_amount=Decimal("0"),
                ),
            )
            for status in DealStatuses
        ]
