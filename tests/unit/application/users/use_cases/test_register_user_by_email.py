from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from commons.operations import AsyncOperation
from mini_crm.application.organizations.services import OrganizationsService
from mini_crm.application.users.entities import User
from mini_crm.application.users.errors import UserWithEmailAlreadyExistsError
from mini_crm.application.users.interfaces import PasswordHasher, UsersRepo
from mini_crm.application.users.use_cases import RegisterUserByEmailUseCase
from tests.unit.application.users.factories import create_register_user_dto


@pytest.fixture(scope="function")
def organizations_service() -> MagicMock:
    return cast(MagicMock, create_autospec(OrganizationsService, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def use_case(
    operation: AsyncOperation,
    users_repo: UsersRepo,
    organizations_service: MagicMock,
    password_hasher: PasswordHasher,
) -> RegisterUserByEmailUseCase:
    return RegisterUserByEmailUseCase(
        operation=operation,
        users_repo=users_repo,
        organizations_service=organizations_service,
        password_hasher=password_hasher,
    )


@pytest.mark.asyncio
async def test__register_user__success_without_organization(
    use_case: RegisterUserByEmailUseCase,
    users_repo: MagicMock,
    password_hasher: MagicMock,
    organizations_service: MagicMock,
) -> None:
    users_repo.exists_by_email.return_value = False
    password_hasher.hash.return_value = "hashed_password"
    dto = create_register_user_dto(organization_name=None)

    await use_case.execute(dto=dto)

    users_repo.add.assert_called_once()
    user: User = users_repo.add.call_args.kwargs["user"]
    assert user.email == "test@example.com"
    assert user.hashed_password == "hashed_password"
    assert user.name == "Test User"
    organizations_service.add_user_to_organization.assert_not_called()


@pytest.mark.asyncio
async def test__register_user__success_with_organization(
    use_case: RegisterUserByEmailUseCase,
    users_repo: MagicMock,
    password_hasher: MagicMock,
    organizations_service: MagicMock,
) -> None:
    users_repo.exists_by_email.return_value = False
    password_hasher.hash.return_value = "hashed_password"
    dto = create_register_user_dto(organization_name="Test Org")

    await use_case.execute(dto=dto)

    users_repo.add.assert_called_once()
    organizations_service.add_user_to_organization.assert_called_once()
    call_kwargs = organizations_service.add_user_to_organization.call_args.kwargs
    assert call_kwargs["organization_name"] == "Test Org"


@pytest.mark.asyncio
async def test__register_user__email_already_exists__raises_error(
    use_case: RegisterUserByEmailUseCase,
    users_repo: MagicMock,
) -> None:
    users_repo.exists_by_email.return_value = True
    dto = create_register_user_dto()

    with pytest.raises(UserWithEmailAlreadyExistsError):
        await use_case.execute(dto=dto)

    users_repo.add.assert_not_called()
