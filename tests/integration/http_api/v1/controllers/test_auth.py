from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from mini_crm.application.users.dtos import LoggedInUserDto
from mini_crm.application.users.use_cases import LoginUserByEmailUseCase, RegisterUserByEmailUseCase


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    register_mock = AsyncMock()
    register_mock.execute = AsyncMock(return_value=None)

    login_mock = AsyncMock()
    login_mock.execute = AsyncMock(return_value=LoggedInUserDto(user_id=1))

    return {
        RegisterUserByEmailUseCase: register_mock,
        LoginUserByEmailUseCase: login_mock,
    }


@pytest.mark.asyncio
async def test__register__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
            "organization_name": "Test Org",
        },
    )

    assert response.status_code == 200
    use_case_mocks[RegisterUserByEmailUseCase].execute.assert_called_once()


@pytest.mark.asyncio
async def test__register__without_organization(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User",
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test__login__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    use_case_mocks[LoginUserByEmailUseCase].execute.assert_called_once()


@pytest.mark.asyncio
async def test__oauth2_login__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/auth/oauth2_login",
        data={
            "username": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    use_case_mocks[LoginUserByEmailUseCase].execute.assert_called_once()
