from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from commons.http_api.auth import JwtManager
from mini_crm.application.activities.use_cases import (
    CreateManualDealActivityUseCase,
    GetActivitiesByDealUseCase,
)
from mini_crm.application.contacts.use_cases import (
    CreateContactUseCase,
    GetContactsByCriteriaUseCase,
)
from mini_crm.application.deals.use_cases import (
    CreateDealUseCase,
    GetDealsFunnelUseCase,
    GetDealsSummaryUseCase,
)
from mini_crm.application.deals.use_cases.update_deal import UpdateDealUseCase
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.organizations.use_cases import (
    GetOrganizationMemberByUserUseCase,
    GetUserOrganizationsUseCase,
)
from mini_crm.application.tasks.use_cases import CreateTaskUseCase, GetTasksByCriteriaUseCase
from mini_crm.application.users.use_cases import RegisterUserByEmailUseCase
from mini_crm.infrastructure.http_api.auth import get_current_user
from mini_crm.infrastructure.http_api.v1 import v1_router


class MockUseCasesProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self, mocks: dict[type, MagicMock]):
        super().__init__()
        self._mocks = mocks

    @provide
    def get_contacts_by_criteria(self) -> GetContactsByCriteriaUseCase:
        return self._mocks.get(GetContactsByCriteriaUseCase, AsyncMock())

    @provide
    def create_contact(self) -> CreateContactUseCase:
        return self._mocks.get(CreateContactUseCase, AsyncMock())

    @provide
    def create_deal(self) -> CreateDealUseCase:
        return self._mocks.get(CreateDealUseCase, AsyncMock())

    @provide
    def update_deal(self) -> UpdateDealUseCase:
        return self._mocks.get(UpdateDealUseCase, AsyncMock())

    @provide
    def get_deals_summary(self) -> GetDealsSummaryUseCase:
        return self._mocks.get(GetDealsSummaryUseCase, AsyncMock())

    @provide
    def get_deals_funnel(self) -> GetDealsFunnelUseCase:
        return self._mocks.get(GetDealsFunnelUseCase, AsyncMock())

    @provide
    def get_tasks_by_criteria(self) -> GetTasksByCriteriaUseCase:
        return self._mocks.get(GetTasksByCriteriaUseCase, AsyncMock())

    @provide
    def create_task(self) -> CreateTaskUseCase:
        return self._mocks.get(CreateTaskUseCase, AsyncMock())

    @provide
    def get_activities_by_deal(self) -> GetActivitiesByDealUseCase:
        return self._mocks.get(GetActivitiesByDealUseCase, AsyncMock())

    @provide
    def create_manual_deal_activity(self) -> CreateManualDealActivityUseCase:
        return self._mocks.get(CreateManualDealActivityUseCase, AsyncMock())

    @provide
    def get_user_organizations(self) -> GetUserOrganizationsUseCase:
        return self._mocks.get(GetUserOrganizationsUseCase, AsyncMock())

    @provide
    def get_organization_member(self) -> GetOrganizationMemberByUserUseCase:
        return self._mocks.get(GetOrganizationMemberByUserUseCase, AsyncMock())

    @provide
    def register_user_by_email(self) -> RegisterUserByEmailUseCase:
        return self._mocks.get(RegisterUserByEmailUseCase, AsyncMock())

    @provide
    def jwt_manager(self) -> JwtManager:
        mock = self._mocks.get(JwtManager)
        if mock:
            return mock

        return JwtManager(
            secret_key="test-secret",
            jwt_algorithm="HS256",
            jwt_access_token_expire_minutes=30,
            jwt_refresh_token_expire_minutes=60 * 24 * 7,
        )


@pytest.fixture
def mock_current_user() -> OrganizationMemberDto:
    """Мок текущего пользователя (owner)"""
    return OrganizationMemberDto(
        user_id=1,
        organization_id=1,
        role=OrganizationMemberRoles.OWNER,
    )


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    """Словарь моков юзкейсов"""
    return {}


@pytest.fixture
def container(use_case_mocks: dict[type, MagicMock]) -> AsyncContainer:
    """Создаёт тестовый контейнер с моками"""
    return make_async_container(MockUseCasesProvider(mocks=use_case_mocks))


@pytest.fixture
def app(mock_current_user: OrganizationMemberDto, container: AsyncContainer) -> FastAPI:
    """Создаёт тестовое приложение с замоканной авторизацией"""
    test_app = FastAPI()
    test_app.include_router(v1_router, prefix="/api")

    async def override_get_current_user() -> OrganizationMemberDto:
        return mock_current_user

    test_app.dependency_overrides[get_current_user] = override_get_current_user

    setup_dishka(container=container, app=test_app)

    return test_app


@pytest_asyncio.fixture
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient]:
    """Создаёт async HTTP client для тестов"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
