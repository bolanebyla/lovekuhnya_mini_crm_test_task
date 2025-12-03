from dataclasses import dataclass

from commons.entities import EntityId
from mini_crm.application.organizations.enums import OrganizationMemberRoles


@dataclass(kw_only=True)
class OrganizationMember:
    """Член организации"""

    id: EntityId
    organization_id: EntityId
    user_id: EntityId
    role: OrganizationMemberRoles
