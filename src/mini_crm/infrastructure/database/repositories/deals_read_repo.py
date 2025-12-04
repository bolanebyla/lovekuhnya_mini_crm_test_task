from sqlalchemy import select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from commons.dtos.pagination import Page
from mini_crm.application.deals.dtos import (
    DealOrderBy,
    DealShortDto,
    GetDealsByCriteriaDto,
    OrderDirection,
)
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.interfaces import DealsReadRepo
from mini_crm.infrastructure.database.tables import deals_table


class DealsReadRepoImpl(BaseReadOnlyRepository, DealsReadRepo):
    async def get_page_by_criteria(
        self,
        criteria: GetDealsByCriteriaDto,
    ) -> Page[DealShortDto]:
        filters = [
            deals_table.c.organization_id == criteria.current_user.organization_id,
        ]

        if criteria.statuses:
            filters.append(deals_table.c.status.in_([status.value for status in criteria.statuses]))

        if criteria.stage is not None:
            filters.append(deals_table.c.stage == criteria.stage.value)

        if criteria.min_amount is not None:
            filters.append(deals_table.c.amount >= criteria.min_amount)

        if criteria.max_amount is not None:
            filters.append(deals_table.c.amount <= criteria.max_amount)

        if criteria.owner_id is not None:
            filters.append(deals_table.c.owner_id == criteria.owner_id)

        order_column = deals_table.c.created_at
        if criteria.order_by == DealOrderBy.AMOUNT:
            order_column = deals_table.c.amount
        elif criteria.order_by == DealOrderBy.UPDATED_AT:
            order_column = deals_table.c.updated_at

        if criteria.order == OrderDirection.DESC:
            order_column_with_direction = order_column.desc()
        else:
            order_column_with_direction = order_column.asc()

        base_query = (
            select(
                deals_table.c.id,
                deals_table.c.contact_id,
                deals_table.c.owner_id,
                deals_table.c.title,
                deals_table.c.amount,
                deals_table.c.currency,
                deals_table.c.status,
                deals_table.c.stage,
                deals_table.c.created_at,
                deals_table.c.updated_at,
            )
            .where(*filters)
            .order_by(order_column_with_direction)
        )

        paginated_query = self.query_builder.add_pagination(
            query=base_query,
            paginated_request=criteria,
        )

        db_items = (await self.session.execute(paginated_query)).mappings().all()

        total = await self.get_total_items(query=base_query)
        pages = self.get_pages_count(total=total, page_size=criteria.page_size)

        items = [
            DealShortDto(
                id=db_item.id,
                contact_id=db_item.contact_id,
                owner_id=db_item.owner_id,
                title=db_item.title,
                amount=db_item.amount,
                currency=db_item.currency,
                status=DealStatuses(db_item.status),
                stage=DealStages(db_item.stage),
                created_at=db_item.created_at,
                updated_at=db_item.updated_at,
            )
            for db_item in db_items
        ]

        return Page(
            items=items,
            page=criteria.page,
            page_size=criteria.page_size,
            total=total,
            pages=pages,
        )
