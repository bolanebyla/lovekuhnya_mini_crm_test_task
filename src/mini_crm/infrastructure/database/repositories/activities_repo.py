from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.activities.entities import Activity
from mini_crm.application.activities.interfaces import ActivitiesRepo


class ActivitiesRepoImpl(BaseRepository, ActivitiesRepo):
    async def add(self, activity: Activity) -> None:
        self.session.add(activity)
        await self.session.flush()
