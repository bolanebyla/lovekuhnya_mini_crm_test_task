import pytest

from commons.operations import AsyncOperation


@pytest.fixture(scope="function")
def operation() -> AsyncOperation:
    return AsyncOperation()
