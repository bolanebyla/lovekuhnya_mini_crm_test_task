from typing import cast

from commons.datetime_utils import now_tz
from commons.entities import EntityId
from mini_crm.application.organizations.entities import Organization
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.organizations.interfaces import OrganizationsRepo
from mini_crm.application.organizations.services.organization_members_service import (
    OrganizationMembersService,
)


class OrganizationsService:
    """Сервис для работы с организациями"""

    def __init__(
        self,
        organizations_repo: OrganizationsRepo,
        organization_members_service: OrganizationMembersService,
    ):
        self._organizations_repo = organizations_repo
        self._organization_members_service = organization_members_service

    async def add_user_to_organization(
        self,
        organization_name: str,
        user_id: EntityId,
    ) -> None:
        """
        Добавляет пользователя в организацию.
        Если организации нет - создаёт и назначает owner
        Если организация есть - добавляет как member
        """
        organization, is_new = await self.get_or_create_organization(name=organization_name)

        role = OrganizationMemberRoles.OWNER if is_new else OrganizationMemberRoles.MEMBER

        await self._organization_members_service.add_member(
            organization_id=cast(EntityId, organization.id),
            user_id=user_id,
            role=role,
        )

    async def get_or_create_organization(self, name: str) -> tuple[Organization, bool]:
        """
        Получает или создаёт организацию по имени.

        Returns:
            tuple[Organization, bool]: (организация, была ли создана новая)
        """
        organization = await self._organizations_repo.get_by_name(name=name)
        if organization is None:
            organization = await self.create_organization(name=name)
            return organization, True
        return organization, False

    async def create_organization(self, name: str) -> Organization:
        """Создаёт новую организацию"""
        organization = Organization(
            name=name,
            created_at=now_tz(),
        )
        await self._organizations_repo.add(organization=organization)
        return organization
