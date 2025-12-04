from pydantic import BaseModel, EmailStr, Field

from mini_crm.application.users.dtos import RegisterUserDto


class RegisterUserSchema(BaseModel):
    """Схема регистрации пользователя"""

    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=8, description="Пароль (минимум 8 символов)")
    name: str = Field(..., description="Имя пользователя")
    organization_name: str | None = Field(None, description="Название организации")

    def to_dto(self) -> RegisterUserDto:
        return RegisterUserDto(
            email=str(self.email),
            password=self.password,
            name=self.name,
            organization_name=self.organization_name,
        )


class LoginSchema(BaseModel):
    """Схема логина"""

    email: EmailStr
    password: str
