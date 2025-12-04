from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from mini_crm.application.deals.use_cases import CreateDealUseCase
from mini_crm.application.deals.use_cases.update_deal import UpdateDealUseCase


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    create_deal_mock = AsyncMock()
    create_deal_mock.execute = AsyncMock(return_value=None)

    update_deal_mock = AsyncMock()
    update_deal_mock.execute = AsyncMock(return_value=None)

    return {
        CreateDealUseCase: create_deal_mock,
        UpdateDealUseCase: update_deal_mock,
    }


@pytest.mark.asyncio
async def test__create_deal__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/deals/",
        json={
            "contact_id": 1,
            "title": "Test Deal",
            "amount": "1000.00",
            "currency": "USD",
        },
    )

    assert response.status_code == 200
    use_case_mocks[CreateDealUseCase].execute.assert_called_once()


@pytest.mark.asyncio
async def test__update_deal__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.patch(
        "/api/v1/deals/1",
        json={
            "status": "in_progress",
            "stage": "proposal",
        },
    )

    assert response.status_code == 200
    use_case_mocks[UpdateDealUseCase].execute.assert_called_once()
