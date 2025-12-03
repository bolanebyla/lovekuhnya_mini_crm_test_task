from fastapi import APIRouter

from mini_crm.infrastructure.http_api.v1.controllers import (
    auth_v1_router,
    contacts_v1_router,
    organizations_v1_router,
)

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_v1_router)
v1_router.include_router(organizations_v1_router)
v1_router.include_router(contacts_v1_router)
