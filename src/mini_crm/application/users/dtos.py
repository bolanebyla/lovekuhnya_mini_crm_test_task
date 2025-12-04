from dataclasses import dataclass


@dataclass(kw_only=True)
class RegisterUserDto:
    """DTO регистрации пользователя"""

    email: str
    password: str
    name: str
    organization_name: str | None = None
