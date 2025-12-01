from sqlalchemy import select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from commons.entities import EntityId
from mini_crm.application.organizations.dtos import UserOrganisationDto
from mini_crm.application.organizations.interfaces import OrganizationsReadRepo
from mini_crm.infrastructure.database.tables import organization_members_table, organizations_table


class OrganizationsReadRepoImpl(BaseReadOnlyRepository, OrganizationsReadRepo):
    async def get_list_by_member_user_id(
        self,
        user_id: EntityId,
    ) -> list[UserOrganisationDto]:
        query = (
            select(organizations_table.c.id, organizations_table.c.name)
            .join(organization_members_table)
            .where(organization_members_table.c.user_id == user_id)
        )

        db_items = (await self.session.execute(query)).mappings().all()

        return [
            UserOrganisationDto(
                id=db_item.id,
                name=db_item.name,
            )
            for db_item in db_items
        ]
