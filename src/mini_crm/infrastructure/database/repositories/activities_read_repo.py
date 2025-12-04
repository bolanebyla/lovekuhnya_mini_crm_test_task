from sqlalchemy import select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from commons.entities import EntityId
from mini_crm.application.activities.dtos import ActivityDto
from mini_crm.application.activities.enums import ActivityTypes
from mini_crm.application.activities.interfaces import ActivitiesReadRepo
from mini_crm.infrastructure.database.tables import activities_table, deals_table


class ActivitiesReadRepoImpl(BaseReadOnlyRepository, ActivitiesReadRepo):
    async def get_by_organization_and_deal_id(
        self,
        organization_id: EntityId,
        deal_id: EntityId,
    ) -> list[ActivityDto]:
        query = (
            select(
                activities_table.c.id,
                activities_table.c.deal_id,
                activities_table.c.author_id,
                activities_table.c.type,
                activities_table.c.payload,
                activities_table.c.created_at,
            )
            .join(deals_table)
            .where(
                activities_table.c.deal_id == deal_id,
                deals_table.c.organization_id == organization_id,
            )
            .order_by(activities_table.c.id)
        )

        db_items = (await self.session.execute(query)).mappings().all()

        return [
            ActivityDto(
                id=db_item.id,
                deal_id=db_item.deal_id,
                author_id=db_item.author_id,
                type=ActivityTypes(db_item.type),
                payload=db_item.payload,
                created_at=db_item.created_at,
            )
            for db_item in db_items
        ]
