from unittest.mock import MagicMock

import pytest

from mini_crm.application.organizations.entities import OrganizationMember
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.organizations.interfaces import OrganizationMembersRepo
from mini_crm.application.organizations.services import OrganizationMembersService


@pytest.fixture(scope="function")
def service(organization_members_repo: OrganizationMembersRepo) -> OrganizationMembersService:
    return OrganizationMembersService(organization_members_repo=organization_members_repo)


@pytest.mark.asyncio
async def test__add_member__success(
    service: OrganizationMembersService,
    organization_members_repo: MagicMock,
) -> None:
    await service.add_member(
        organization_id=1,
        user_id=2,
        role=OrganizationMemberRoles.MEMBER,
    )

    organization_members_repo.add.assert_called_once()
    member: OrganizationMember = organization_members_repo.add.call_args.kwargs[
        "organization_member"
    ]
    assert member.organization_id == 1
    assert member.user_id == 2
    assert member.role == OrganizationMemberRoles.MEMBER
