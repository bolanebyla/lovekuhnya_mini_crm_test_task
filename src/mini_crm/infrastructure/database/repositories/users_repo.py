from sqlalchemy import exists, select

from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.users.entities import User
from mini_crm.application.users.interfaces import UsersRepo
from mini_crm.infrastructure.database.tables import users_table


class UsersRepoImpl(BaseRepository, UsersRepo):
    async def add(self, user: User) -> None:
        self.session.add(user)
        await self.session.flush()

    async def exists_by_email(self, email: str) -> bool:
        query = select(exists().where(users_table.c.email == email))
        result = await self.session.execute(query)
        return result.scalar_one()

    async def get_by_email(self, email: str) -> User | None:
        query = select(User).where(users_table.c.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
