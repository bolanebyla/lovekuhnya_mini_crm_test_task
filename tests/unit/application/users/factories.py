from mini_crm.application.users.dtos import RegisterUserDto


def create_register_user_dto(
    email: str = "test@example.com",
    password: str = "password123",
    name: str = "Test User",
    organization_name: str | None = None,
) -> RegisterUserDto:
    return RegisterUserDto(
        email=email,
        password=password,
        name=name,
        organization_name=organization_name,
    )
