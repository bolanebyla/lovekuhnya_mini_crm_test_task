from typing import cast

from commons.datetime_utils import now_tz
from commons.entities import EntityId
from commons.operations import AsyncOperation, async_operation
from mini_crm.application.organizations.services import OrganizationsService
from mini_crm.application.users.dtos import RegisterUserDto
from mini_crm.application.users.entities import User
from mini_crm.application.users.errors import UserWithEmailAlreadyExistsError
from mini_crm.application.users.interfaces import PasswordHasher, UsersRepo


class RegisterUserByEmailUseCase:
    """Регистрация пользователя"""

    def __init__(
        self,
        operation: AsyncOperation,
        users_repo: UsersRepo,
        organizations_service: OrganizationsService,
        password_hasher: PasswordHasher,
    ):
        self._operation = operation
        self._users_repo = users_repo
        self._organizations_service = organizations_service
        self._password_hasher = password_hasher

    @async_operation
    async def execute(self, dto: RegisterUserDto) -> None:
        user_exists_by_email = await self._users_repo.exists_by_email(email=dto.email)
        if user_exists_by_email:
            raise UserWithEmailAlreadyExistsError(email=dto.email)

        hashed_password = self._password_hasher.hash(password=dto.password)

        user = User(
            email=dto.email,
            hashed_password=hashed_password,
            name=dto.name,
            created_at=now_tz(),
        )
        await self._users_repo.add(user=user)

        if dto.organization_name is not None:
            await self._organizations_service.add_user_to_organization(
                organization_name=dto.organization_name,
                user_id=cast(EntityId, user.id),
            )
