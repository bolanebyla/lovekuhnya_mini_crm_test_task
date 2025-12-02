from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from commons.http_api.auth import JwtManager

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)


class CurrentUser(BaseModel):
    """Текущий пользователь"""

    user_id: int


@inject
def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    jwt_manager: FromDishka[JwtManager],
) -> CurrentUser:
    token_claims = jwt_manager.verify_access_token(token=access_token)
    current_client = CurrentUser(
        user_id=int(token_claims.sub),
    )
    return current_client
