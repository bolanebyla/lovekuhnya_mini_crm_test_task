from dataclasses import dataclass

from commons.entities import EntityId


@dataclass(kw_only=True)
class RegisterUserDto:
    """DTO регистрации пользователя"""

    email: str
    password: str
    name: str
    organization_name: str | None = None


@dataclass(kw_only=True)
class LoginUserDto:
    """DTO входа пользователя"""

    email: str
    password: str


@dataclass(kw_only=True)
class LoggedInUserDto:
    """DTO авторизованного пользователя"""

    user_id: EntityId
