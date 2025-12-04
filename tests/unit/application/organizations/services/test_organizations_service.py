from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from mini_crm.application.organizations.entities import Organization
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.organizations.interfaces import OrganizationsRepo
from mini_crm.application.organizations.services import (
    OrganizationMembersService,
    OrganizationsService,
)
from tests.unit.factories import create_organization


@pytest.fixture(scope="function")
def organization_members_service() -> MagicMock:
    return cast(
        MagicMock, create_autospec(OrganizationMembersService, spec_set=True, instance=True)
    )


@pytest.fixture(scope="function")
def service(
    organizations_repo: OrganizationsRepo,
    organization_members_service: MagicMock,
) -> OrganizationsService:
    return OrganizationsService(
        organizations_repo=organizations_repo,
        organization_members_service=organization_members_service,
    )


@pytest.mark.asyncio
async def test__create_organization__success(
    service: OrganizationsService,
    organizations_repo: MagicMock,
) -> None:
    result = await service.create_organization(name="Test Org")

    organizations_repo.add.assert_called_once()
    organization: Organization = organizations_repo.add.call_args.kwargs["organization"]
    assert organization.name == "Test Org"
    assert result.name == "Test Org"


@pytest.mark.asyncio
async def test__get_or_create_organization__organization_exists__returns_existing(
    service: OrganizationsService,
    organizations_repo: MagicMock,
) -> None:
    existing_org = create_organization(name="Existing Org")
    organizations_repo.get_by_name.return_value = existing_org

    result, is_new = await service.get_or_create_organization(name="Existing Org")

    assert result == existing_org
    assert is_new is False
    organizations_repo.add.assert_not_called()


@pytest.mark.asyncio
async def test__get_or_create_organization__organization_not_exists__creates_new(
    service: OrganizationsService,
    organizations_repo: MagicMock,
) -> None:
    organizations_repo.get_by_name.return_value = None

    result, is_new = await service.get_or_create_organization(name="New Org")

    assert result.name == "New Org"
    assert is_new is True
    organizations_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__add_user_to_organization__new_organization__creates_as_owner(
    service: OrganizationsService,
    organizations_repo: MagicMock,
    organization_members_service: MagicMock,
) -> None:
    organizations_repo.get_by_name.return_value = None

    await service.add_user_to_organization(
        organization_name="New Org",
        user_id=1,
    )

    organization_members_service.add_member.assert_called_once()
    call_kwargs = organization_members_service.add_member.call_args.kwargs
    assert call_kwargs["user_id"] == 1
    assert call_kwargs["role"] == OrganizationMemberRoles.OWNER


@pytest.mark.asyncio
async def test__add_user_to_organization__existing_organization__adds_as_member(
    service: OrganizationsService,
    organizations_repo: MagicMock,
    organization_members_service: MagicMock,
) -> None:
    existing_org = create_organization(name="Existing Org")
    organizations_repo.get_by_name.return_value = existing_org

    await service.add_user_to_organization(
        organization_name="Existing Org",
        user_id=1,
    )

    organization_members_service.add_member.assert_called_once()
    call_kwargs = organization_members_service.add_member.call_args.kwargs
    assert call_kwargs["user_id"] == 1
    assert call_kwargs["role"] == OrganizationMemberRoles.MEMBER
