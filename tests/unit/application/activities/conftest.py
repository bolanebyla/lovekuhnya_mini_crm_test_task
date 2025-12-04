from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from mini_crm.application.activities.interfaces import ActivitiesRepo


@pytest.fixture(scope="function")
def activities_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(ActivitiesRepo, spec_set=True, instance=True))
