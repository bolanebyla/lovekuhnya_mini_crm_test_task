from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from commons.dtos.pagination import Page
from mini_crm.application.deals.dtos import DealShortDto
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.use_cases import CreateDealUseCase, GetDealsByCriteriaUseCase
from mini_crm.application.deals.use_cases.update_deal import UpdateDealUseCase


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    get_deals_mock = AsyncMock()
    get_deals_mock.execute = AsyncMock(
        return_value=Page(
            items=[
                DealShortDto(
                    id=1,
                    contact_id=1,
                    owner_id=1,
                    title="Test Deal",
                    amount=Decimal("1000.00"),
                    currency="USD",
                    status=DealStatuses.NEW,
                    stage=DealStages.QUALIFICATION,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            ],
            page=1,
            page_size=20,
            total=1,
            pages=1,
        )
    )

    create_deal_mock = AsyncMock()
    create_deal_mock.execute = AsyncMock(return_value=None)

    update_deal_mock = AsyncMock()
    update_deal_mock.execute = AsyncMock(return_value=None)

    return {
        GetDealsByCriteriaUseCase: get_deals_mock,
        CreateDealUseCase: create_deal_mock,
        UpdateDealUseCase: update_deal_mock,
    }


@pytest.mark.asyncio
async def test__get_deals__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get("/api/v1/deals/")

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Test Deal"
    assert data["page"] == 1
    assert data["total"] == 1


@pytest.mark.asyncio
async def test__get_deals__with_filters(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get(
        "/api/v1/deals/",
        params={
            "status": ["new", "in_progress"],
            "stage": "proposal",
            "min_amount": "100",
            "max_amount": "10000",
            "order_by": "amount",
            "order": "asc",
        },
    )

    assert response.status_code == 200
    use_case_mocks[GetDealsByCriteriaUseCase].execute.assert_called_once()


@pytest.mark.asyncio
async def test__get_deals__with_pagination(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get(
        "/api/v1/deals/",
        params={"page": 2, "page_size": 10},
    )

    assert response.status_code == 200


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
async def test__create_deal__validation_error(
    client: AsyncClient,
) -> None:
    response = await client.post(
        "/api/v1/deals/",
        json={
            "title": "Test Deal",
            # missing contact_id, amount, currency
        },
    )

    assert response.status_code == 422


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


@pytest.mark.asyncio
async def test__update_deal__invalid_status(
    client: AsyncClient,
) -> None:
    response = await client.patch(
        "/api/v1/deals/1",
        json={
            "status": "invalid_status",
            "stage": "proposal",
        },
    )

    assert response.status_code == 422
