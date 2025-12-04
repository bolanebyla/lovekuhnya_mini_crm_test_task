from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from mini_crm.application.users.interfaces import PasswordHasher, UsersRepo


@pytest.fixture(scope="function")
def users_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(UsersRepo, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def password_hasher() -> MagicMock:
    return cast(MagicMock, create_autospec(PasswordHasher, spec_set=True, instance=True))
