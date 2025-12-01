from dataclasses import dataclass

from commons.entities import EntityId


@dataclass(kw_only=True)
class OrganizationMember:
    """Член организации"""

    id: EntityId
    organization_id: EntityId
    user_id: EntityId
    role: str  # TODO: enum
