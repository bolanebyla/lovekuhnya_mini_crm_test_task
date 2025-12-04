from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from mini_crm.application.organizations.dtos import UserOrganizationDto
from mini_crm.application.organizations.use_cases import GetUserOrganizationsUseCase


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    get_organizations_mock = AsyncMock()
    get_organizations_mock.execute = AsyncMock(
        return_value=[
            UserOrganizationDto(
                id=1,
                name="Test Organization",
            ),
            UserOrganizationDto(
                id=2,
                name="Another Organization",
            ),
        ]
    )

    return {
        GetUserOrganizationsUseCase: get_organizations_mock,
    }


@pytest.mark.asyncio
async def test__get_user_organizations__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get("/api/v1/organizations/me")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Organization"
    assert data[1]["name"] == "Another Organization"
