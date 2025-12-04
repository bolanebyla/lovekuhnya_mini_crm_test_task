"""Интеграционные тесты для контроллера contacts"""

from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from commons.dtos.pagination import Page
from mini_crm.application.contacts.dtos import ContactShortDto
from mini_crm.application.contacts.use_cases import (
    CreateContactUseCase,
    GetContactsByCriteriaUseCase,
)


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    """Моки юзкейсов для contacts"""
    get_contacts_mock = AsyncMock()
    get_contacts_mock.execute = AsyncMock(
        return_value=Page(
            items=[
                ContactShortDto(
                    id=1,
                    name="John Doe",
                    email="john@example.com",
                    phone="+1234567890",
                )
            ],
            page=1,
            page_size=20,
            total=1,
            pages=1,
        )
    )

    create_contact_mock = AsyncMock()
    create_contact_mock.execute = AsyncMock(return_value=None)

    return {
        GetContactsByCriteriaUseCase: get_contacts_mock,
        CreateContactUseCase: create_contact_mock,
    }


@pytest.mark.asyncio
async def test__get_contacts__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get(
        "/api/v1/contacts/",
        params={"page": 1, "page_size": 1},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "John Doe"


@pytest.mark.asyncio
async def test__get_contacts__with_pagination(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get(
        "/api/v1/contacts/",
        params={"page": 1, "page_size": 10},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["page_size"] == 20


@pytest.mark.asyncio
async def test__create_contact__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/contacts/",
        json={
            "name": "New Contact",
            "email": "new@example.com",
            "phone": "+1234567890",
        },
    )

    assert response.status_code == 200
    use_case_mocks[CreateContactUseCase].execute.assert_called_once()
