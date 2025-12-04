from commons.entities import EntityId
from mini_crm.application.organizations.entities import OrganizationMember
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.organizations.interfaces import OrganizationMembersRepo


class OrganizationMembersService:
    """Сервис для работы с участниками организации"""

    def __init__(self, organization_members_repo: OrganizationMembersRepo):
        self._organization_members_repo = organization_members_repo

    async def add_member(
        self,
        organization_id: EntityId,
        user_id: EntityId,
        role: OrganizationMemberRoles,
    ) -> None:
        """Добавляет пользователя в организацию"""
        organization_member = OrganizationMember(
            organization_id=organization_id,
            user_id=user_id,
            role=role,
        )
        await self._organization_members_repo.add(organization_member=organization_member)
