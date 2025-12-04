from typing import cast

from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.users.dtos import LoggedInUserDto, LoginUserDto
from mini_crm.application.users.errors import InvalidCredentialsError
from mini_crm.application.users.interfaces import PasswordHasher, UsersRepo


class LoginUserByEmailUseCase:
    """Вход пользователя по email и паролю"""

    def __init__(
        self,
        operation: AsyncOperation,
        users_repo: UsersRepo,
        password_hasher: PasswordHasher,
    ):
        self._operation = operation
        self._users_repo = users_repo
        self._password_hasher = password_hasher

    @async_operation
    async def execute(self, dto: LoginUserDto) -> LoggedInUserDto:
        user = await self._users_repo.get_by_email(email=dto.email)

        if user is None:
            raise InvalidCredentialsError()

        is_password_valid = self._password_hasher.verify(
            password=dto.password,
            hashed_password=user.hashed_password,
        )

        if not is_password_valid:
            raise InvalidCredentialsError()

        return LoggedInUserDto(user_id=cast(EntityId, user.id))
