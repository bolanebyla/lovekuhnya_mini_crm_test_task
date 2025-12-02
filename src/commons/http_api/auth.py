from datetime import UTC, datetime, timedelta
from enum import StrEnum

from fastapi import HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel, Field, ValidationError
from starlette import status

from commons.entities.base import EntityId


class JwtTokenTypes(StrEnum):
    """
    Типы jwt токенов
    """

    ACCESS = "access"
    REFRESH = "refresh"


class JwtTokenClaims(BaseModel):
    """
    Полезные данные jwt токена
    """

    exp: datetime = Field(..., title="Дата истечения токена")
    type: JwtTokenTypes = Field(..., title="Тип токена")
    sub: str = Field(..., title="Id пользователя")


class AuthTokensResponseTypes(StrEnum):
    """
    Типы токенов авторизации
    """

    BEARER = "bearer"


class AuthTokensResponse(BaseModel):
    """
    Токены авторизации
    """

    access_token: str
    refresh_token: str
    token_type: AuthTokensResponseTypes


class JwtManager:
    """
    Класс для управления jwt
    """

    def __init__(
        self,
        secret_key: str,
        jwt_algorithm: str,
        jwt_access_token_expire_minutes: int | float,
        jwt_refresh_token_expire_minutes: int | float,
    ):
        self._secret_key = secret_key
        self._jwt_algorithm = jwt_algorithm
        self._jwt_access_token_expire_minutes = jwt_access_token_expire_minutes
        self._jwt_refresh_token_expire_minutes = jwt_refresh_token_expire_minutes

    def create_auth_tokens(
        self,
        user_id: int,
    ) -> AuthTokensResponse:
        access_token = self.create_access_token(
            user_id=user_id,
        )
        refresh_token = self.create_refresh_token(
            user_id=user_id,
        )
        return AuthTokensResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=AuthTokensResponseTypes.BEARER,
        )

    def create_access_token(
        self,
        user_id: EntityId,
    ) -> str:
        """
        Создаёт токен jwt access токен
        """
        expire = datetime.now(UTC) + timedelta(minutes=self._jwt_access_token_expire_minutes)
        access_token = self._create_token(
            user_id=user_id,
            expire=expire,
            token_type=JwtTokenTypes.ACCESS,
        )
        return access_token

    def create_refresh_token(self, user_id: EntityId) -> str:
        """
        Создаёт jwt refresh токен
        """
        expire = datetime.now(UTC) + timedelta(minutes=self._jwt_refresh_token_expire_minutes)
        refresh_token = self._create_token(
            user_id=user_id,
            expire=expire,
            token_type=JwtTokenTypes.REFRESH,
        )
        return refresh_token

    def _create_token(
        self,
        user_id: EntityId,
        expire: datetime,
        token_type: JwtTokenTypes,
    ) -> str:
        """
        Создаёт jwt токен
        """
        jwt_token_claims = JwtTokenClaims(
            type=token_type,
            exp=expire,
            sub=str(user_id),
        )

        encoded_jwt: str = jwt.encode(
            jwt_token_claims.model_dump(),
            self._secret_key,
            algorithm=self._jwt_algorithm,
        )
        return encoded_jwt

    def verify_access_token(self, token: str) -> JwtTokenClaims:
        jwt_token_claims = self._decode_jwt(token)

        if jwt_token_claims.type != JwtTokenTypes.ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Only {JwtTokenTypes.ACCESS} tokens are allowed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return jwt_token_claims

    def verify_refresh_token(self, token: str) -> JwtTokenClaims:
        jwt_token_claims = self._decode_jwt(token)

        if jwt_token_claims.type != JwtTokenTypes.REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Only {JwtTokenTypes.REFRESH} tokens are allowed",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return jwt_token_claims

    def _decode_jwt(self, token: str) -> JwtTokenClaims:
        """
        Декодирует jwt токен и получает полезную нагрузку
        """

        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._jwt_algorithm],
            )

            jwt_token_claims = JwtTokenClaims(**payload)

        except (JWTError, ValidationError) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

        return jwt_token_claims
