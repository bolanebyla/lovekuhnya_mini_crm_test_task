from datetime import datetime

from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.entities import Organization
from mini_crm.application.organizations.enums import OrganizationMemberRoles


def create_organization_member(
    user_id: int = 1,
    organization_id: int = 1,
    role: OrganizationMemberRoles = OrganizationMemberRoles.MEMBER,
) -> OrganizationMemberDto:
    return OrganizationMemberDto(
        user_id=user_id,
        organization_id=organization_id,
        role=role,
    )


def create_organization(
    id_: int = 1,
    name: str = "Test Organization",
    created_at: datetime | None = None,
) -> Organization:
    return Organization(
        id=id_,
        name=name,
        created_at=created_at or datetime(day=1, month=12, year=2025),
    )
