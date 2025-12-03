from sqlalchemy import select

from commons.db.sqlalchemy import BaseReadOnlyRepository
from commons.entities import EntityId
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.interfaces import OrganizationMembersReadRepo
from mini_crm.infrastructure.database.tables import organization_members_table


class OrganizationMembersReadRepoImpl(BaseReadOnlyRepository, OrganizationMembersReadRepo):
    async def get_by_organization_and_user_id(
        self,
        organization_id: EntityId,
        user_id: EntityId,
    ) -> OrganizationMemberDto | None:
        base_query = select(
            organization_members_table.c.user_id,
            organization_members_table.c.organization_id,
            organization_members_table.c.role,
        ).where(
            organization_members_table.c.organization_id == organization_id,
            organization_members_table.c.user_id == user_id,
        )

        db_item = (await self.session.execute(base_query)).mappings().one_or_none()

        return (
            OrganizationMemberDto(
                user_id=db_item.user_id,
                organization_id=db_item.organization_id,
                role=db_item.role,
            )
            if db_item
            else None
        )
