from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from commons.http_api.auth import AuthTokensResponse, JwtManager
from mini_crm.application.users.dtos import LoginUserDto
from mini_crm.application.users.use_cases import LoginUserByEmailUseCase, RegisterUserByEmailUseCase
from mini_crm.infrastructure.http_api.v1.schemas import LoginSchema, RegisterUserSchema

auth_v1_router = APIRouter(
    prefix="/auth",
    route_class=DishkaRoute,
    tags=["Auth"],
)


@auth_v1_router.post("/register")
async def register(
    register_schema: Annotated[RegisterUserSchema, Body()],
    use_case: FromDishka[RegisterUserByEmailUseCase],
) -> None:
    """Регистрация пользователя и первой организации"""
    dto = register_schema.to_dto()
    await use_case.execute(dto=dto)


@auth_v1_router.post("/oauth2_login")
async def oauth2_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: FromDishka[LoginUserByEmailUseCase],
    jwt_manager: FromDishka[JwtManager],
) -> AuthTokensResponse:
    """Вход для OAuth2"""
    dto = LoginUserDto(email=form_data.username, password=form_data.password)
    logged_in_user = await use_case.execute(dto=dto)

    return jwt_manager.create_auth_tokens(user_id=str(logged_in_user.user_id))


@auth_v1_router.post("/login")
async def login(
    login_schema: Annotated[LoginSchema, Body()],
    use_case: FromDishka[LoginUserByEmailUseCase],
    jwt_manager: FromDishka[JwtManager],
) -> AuthTokensResponse:
    """Вход по email и паролю"""
    dto = login_schema.to_dto()
    logged_in_user = await use_case.execute(dto=dto)

    return jwt_manager.create_auth_tokens(user_id=str(logged_in_user.user_id))
