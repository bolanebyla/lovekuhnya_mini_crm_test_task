from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from commons.http_api.auth import AuthTokensResponse, JwtManager

auth_v1_router = APIRouter(
    prefix="/auth",
    route_class=DishkaRoute,
    tags=["Auth"],
)


@auth_v1_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    jwt_manager: FromDishka[JwtManager],
) -> AuthTokensResponse:
    """
    Вход по парою
    """
    # TODO: получать пользователя по email и паролю
    jwt_tokens = jwt_manager.create_auth_tokens(
        user_id=1,
    )
    return jwt_tokens
