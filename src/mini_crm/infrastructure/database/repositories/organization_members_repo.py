from commons.db.sqlalchemy import BaseRepository
from mini_crm.application.organizations.entities import OrganizationMember
from mini_crm.application.organizations.interfaces import OrganizationMembersRepo


class OrganizationMembersRepoImpl(BaseRepository, OrganizationMembersRepo):
    async def add(self, organization_member: OrganizationMember) -> None:
        self.session.add(organization_member)
        await self.session.flush()
