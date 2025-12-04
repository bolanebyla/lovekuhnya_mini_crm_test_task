from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from mini_crm.application.organizations.interfaces import (
    OrganizationMembersRepo,
    OrganizationsReadRepo,
    OrganizationsRepo,
)


@pytest.fixture(scope="function")
def organizations_read_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(OrganizationsReadRepo, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def organizations_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(OrganizationsRepo, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def organization_members_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(OrganizationMembersRepo, spec_set=True, instance=True))
