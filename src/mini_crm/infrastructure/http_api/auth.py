from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer

from commons.http_api.auth import JwtManager
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.errors import (
    OrganizationMemberNotFoundByOrganizationIdAndUserId,
)
from mini_crm.application.organizations.use_cases import GetOrganizationMemberByUserUseCase

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/oauth2_login",
)


@inject
async def get_current_user(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    organization_id: Annotated[int, Header(alias="X-Organization-Id")],
    jwt_manager: FromDishka[JwtManager],
    get_organization_member_use_case: FromDishka[GetOrganizationMemberByUserUseCase],
) -> OrganizationMemberDto:
    token_claims = jwt_manager.verify_access_token(token=access_token)

    try:
        organization_member = await get_organization_member_use_case.execute(
            organization_id=organization_id,
            user_id=int(token_claims.sub),
        )
    except OrganizationMemberNotFoundByOrganizationIdAndUserId as e:
        raise HTTPException(
            status_code=403,
        ) from e

    return organization_member


@inject
def get_current_user_id(
    access_token: Annotated[str, Depends(oauth2_scheme)],
    jwt_manager: FromDishka[JwtManager],
) -> int:
    token_claims = jwt_manager.verify_access_token(token=access_token)
    return int(token_claims.sub)
