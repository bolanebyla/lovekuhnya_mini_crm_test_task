from dataclasses import dataclass

from commons.entities import EntityId
from mini_crm.application.organizations.enums import OrganizationMemberRoles


@dataclass(kw_only=True)
class UserOrganizationDto:
    """Организация пользователя"""

    id: EntityId
    name: str


@dataclass(kw_only=True)
class OrganizationMemberDto:
    """Член организации"""

    user_id: EntityId
    organization_id: EntityId
    role: OrganizationMemberRoles
