from datetime import datetime
from decimal import Decimal

from sqlalchemy import func, select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from commons.entities import EntityId
from mini_crm.application.deals.dtos import DealStatusSummaryDto
from mini_crm.application.deals.enums import DealStatuses
from mini_crm.application.deals.interfaces import DealsAnalyticsRepo
from mini_crm.infrastructure.database.tables import deals_table


class DealsAnalyticsRepoImpl(BaseReadOnlyRepository, DealsAnalyticsRepo):
    async def get_summary_by_status(
        self,
        organization_id: EntityId,
    ) -> list[DealStatusSummaryDto]:
        query = (
            select(
                deals_table.c.status,
                func.count().label("count"),
                func.coalesce(func.sum(deals_table.c.amount), 0).label("total_amount"),
            )
            .where(deals_table.c.organization_id == organization_id)
            .group_by(deals_table.c.status)
        )

        result = await self.session.execute(query)
        rows = result.mappings().all()

        return [
            DealStatusSummaryDto(
                status=DealStatuses(row.status),
                count=row.count,
                total_amount=Decimal(row.total_amount),
            )
            for row in rows
        ]

    async def get_won_average_amount(
        self,
        organization_id: EntityId,
    ) -> Decimal | None:
        query = select(func.avg(deals_table.c.amount)).where(
            deals_table.c.organization_id == organization_id,
            deals_table.c.status == DealStatuses.WON,
        )

        result = await self.session.execute(query)
        avg = result.scalar_one_or_none()

        return Decimal(avg) if avg is not None else None

    async def get_new_deals_count(
        self,
        organization_id: EntityId,
        since: datetime,
    ) -> int:
        query = (
            select(func.count())
            .select_from(deals_table)
            .where(
                deals_table.c.organization_id == organization_id,
                deals_table.c.created_at >= since,
            )
        )

        result = await self.session.execute(query)
        return result.scalar_one()
