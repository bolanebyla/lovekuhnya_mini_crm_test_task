from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from mini_crm.application.deals.interfaces import DealsRepo


@pytest.fixture(scope="function")
def deals_repo() -> MagicMock:
    return cast(MagicMock, create_autospec(DealsRepo, spec_set=True, instance=True))
