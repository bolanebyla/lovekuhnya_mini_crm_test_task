"""Интеграционные тесты для JWT"""

import pytest
from fastapi import HTTPException

from commons.http_api.auth import JwtManager, JwtTokenTypes


@pytest.fixture
def jwt_manager() -> JwtManager:
    return JwtManager(
        secret_key="test-secret-key",
        jwt_algorithm="HS256",
        jwt_access_token_expire_minutes=30,
        jwt_refresh_token_expire_minutes=60 * 24 * 7,
    )


def test__create_access_token__returns_valid_token(jwt_manager: JwtManager) -> None:
    token = jwt_manager.create_access_token(user_id=1)

    assert token is not None
    assert isinstance(token, str)


def test__verify_access_token__valid_token__returns_claims(jwt_manager: JwtManager) -> None:
    token = jwt_manager.create_access_token(user_id=42)

    claims = jwt_manager.verify_access_token(token=token)

    assert claims.sub == "42"
    assert claims.type == JwtTokenTypes.ACCESS


def test__verify_access_token__invalid_token__raises_error(jwt_manager: JwtManager) -> None:
    with pytest.raises(HTTPException) as exc_info:
        jwt_manager.verify_access_token(token="invalid-token")

    assert exc_info.value.status_code == 401


def test__verify_access_token__refresh_token__raises_error(jwt_manager: JwtManager) -> None:
    refresh_token = jwt_manager.create_refresh_token(user_id=1)

    with pytest.raises(HTTPException) as exc_info:
        jwt_manager.verify_access_token(token=refresh_token)

    assert exc_info.value.status_code == 401


def test__create_auth_tokens__returns_both_tokens(jwt_manager: JwtManager) -> None:
    tokens = jwt_manager.create_auth_tokens(user_id=1)

    assert tokens.access_token is not None
    assert tokens.refresh_token is not None
    assert tokens.token_type.value == "bearer"


def test__verify_refresh_token__valid_token__returns_claims(jwt_manager: JwtManager) -> None:
    token = jwt_manager.create_refresh_token(user_id=42)

    claims = jwt_manager.verify_refresh_token(token=token)

    assert claims.sub == "42"
    assert claims.type == JwtTokenTypes.REFRESH


def test__verify_refresh_token__access_token__raises_error(jwt_manager: JwtManager) -> None:
    access_token = jwt_manager.create_access_token(user_id=1)

    with pytest.raises(HTTPException) as exc_info:
        jwt_manager.verify_refresh_token(token=access_token)

    assert exc_info.value.status_code == 401
