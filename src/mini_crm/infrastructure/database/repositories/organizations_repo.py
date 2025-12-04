from sqlalchemy import select

from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.organizations.entities import Organization
from mini_crm.application.organizations.interfaces import OrganizationsRepo
from mini_crm.infrastructure.database.tables import organizations_table


class OrganizationsRepoImpl(BaseRepository, OrganizationsRepo):
    async def add(self, organization: Organization) -> None:
        self.session.add(organization)
        await self.session.flush()

    async def get_by_name(self, name: str) -> Organization | None:
        query = select(Organization).where(organizations_table.c.name == name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
