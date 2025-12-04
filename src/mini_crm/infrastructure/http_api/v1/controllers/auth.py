from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm

from commons.http_api.auth import AuthTokensResponse, JwtManager
from mini_crm.infrastructure.http_api.v1.schemas import LoginSchema

auth_v1_router = APIRouter(
    prefix="/auth",
    route_class=DishkaRoute,
    tags=["Auth"],
)


@auth_v1_router.post("/oauth2_login")
async def oauth2_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    jwt_manager: FromDishka[JwtManager],
) -> AuthTokensResponse:
    # TODO: получать пользователя по email и паролю
    jwt_tokens = jwt_manager.create_auth_tokens(
        user_id=1,
    )
    return jwt_tokens


@auth_v1_router.post("/login")
async def login(
    login_schema: Annotated[LoginSchema, Body()],
    jwt_manager: FromDishka[JwtManager],
) -> AuthTokensResponse:
    """
    Вход по email и парою
    """
    # TODO: получать пользователя по email и паролю
    jwt_tokens = jwt_manager.create_auth_tokens(
        user_id=1,
    )
    return jwt_tokens
