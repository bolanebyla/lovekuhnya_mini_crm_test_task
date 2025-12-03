from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.deals.entities import Deal
from mini_crm.application.deals.interfaces import DealsRepo


class DealsRepoImpl(BaseRepository, DealsRepo):
    async def add(self, deal: Deal) -> None:
        self.session.add(deal)
        await self.session.flush()
