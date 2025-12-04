from datetime import datetime

import pytest

from commons.operations import AsyncOperation


@pytest.fixture(scope="function")
def operation() -> AsyncOperation:
    return AsyncOperation()


@pytest.fixture(scope="function")
def frozen_datetime() -> datetime:
    return datetime(day=1, month=12, year=2025)
