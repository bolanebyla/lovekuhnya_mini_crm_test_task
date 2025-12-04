from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest

from commons.operations import AsyncOperation
from mini_crm.application.users.dtos import LoginUserDto
from mini_crm.application.users.entities import User
from mini_crm.application.users.errors import InvalidCredentialsError
from mini_crm.application.users.interfaces import PasswordHasher, UsersRepo
from mini_crm.application.users.use_cases import LoginUserByEmailUseCase


@pytest.fixture
def operation() -> MagicMock:
    return create_autospec(AsyncOperation, instance=True)


@pytest.fixture
def users_repo() -> AsyncMock:
    return create_autospec(UsersRepo, instance=True)


@pytest.fixture
def password_hasher() -> MagicMock:
    return create_autospec(PasswordHasher, instance=True)


@pytest.fixture
def use_case(
    operation: MagicMock,
    users_repo: AsyncMock,
    password_hasher: MagicMock,
) -> LoginUserByEmailUseCase:
    return LoginUserByEmailUseCase(
        operation=operation,
        users_repo=users_repo,
        password_hasher=password_hasher,
    )


def _create_user() -> User:
    user = User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        name="Test User",
        created_at=datetime.now(),
    )
    return user


def _create_dto(
    email: str = "test@example.com",
    password: str = "password123",
) -> LoginUserDto:
    return LoginUserDto(email=email, password=password)


@pytest.mark.asyncio
async def test__execute__success(
    use_case: LoginUserByEmailUseCase,
    users_repo: AsyncMock,
    password_hasher: MagicMock,
) -> None:
    user = _create_user()
    users_repo.get_by_email.return_value = user
    password_hasher.verify.return_value = True

    dto = _create_dto()
    result = await use_case.execute(dto=dto)

    assert result.user_id == 1
    users_repo.get_by_email.assert_called_once_with(email="test@example.com")
    password_hasher.verify.assert_called_once_with(
        password="password123",
        hashed_password="hashed_password",
    )


@pytest.mark.asyncio
async def test__execute__user_not_found__raises_invalid_credentials(
    use_case: LoginUserByEmailUseCase,
    users_repo: AsyncMock,
    password_hasher: MagicMock,
) -> None:
    users_repo.get_by_email.return_value = None

    dto = _create_dto()

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(dto=dto)

    password_hasher.verify.assert_not_called()


@pytest.mark.asyncio
async def test__execute__wrong_password__raises_invalid_credentials(
    use_case: LoginUserByEmailUseCase,
    users_repo: AsyncMock,
    password_hasher: MagicMock,
) -> None:
    user = _create_user()
    users_repo.get_by_email.return_value = user
    password_hasher.verify.return_value = False

    dto = _create_dto()

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(dto=dto)
