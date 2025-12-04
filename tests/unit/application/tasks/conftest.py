from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from mini_crm.application.tasks.interfaces import TasksRepo


@pytest.fixture(scope="function")
def tasks_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(TasksRepo, spec_set=True, instance=True))
