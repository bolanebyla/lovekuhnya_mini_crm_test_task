from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from commons.app_errors.errors import ForbiddenUserActionError
from commons.dtos.pagination import Page
from commons.operations import AsyncOperation
from mini_crm.application.deals.dtos import DealShortDto, GetDealsByCriteriaDto
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.interfaces import DealsReadRepo
from mini_crm.application.deals.use_cases import GetDealsByCriteriaUseCase
from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.enums import OrganizationMemberRoles


@pytest.fixture
def use_case(
    operation: AsyncOperation, deals_read_repo: DealsReadRepo
) -> GetDealsByCriteriaUseCase:
    return GetDealsByCriteriaUseCase(
        operation=operation,
        deals_read_repo=deals_read_repo,
    )


def _create_current_user(
    role: OrganizationMemberRoles = OrganizationMemberRoles.OWNER,
) -> OrganizationMemberDto:
    return OrganizationMemberDto(
        user_id=1,
        organization_id=1,
        role=role,
    )


def _create_criteria(
    owner_id: int | None = None,
    role: OrganizationMemberRoles = OrganizationMemberRoles.OWNER,
) -> GetDealsByCriteriaDto:
    return GetDealsByCriteriaDto(
        page=1,
        page_size=20,
        owner_id=owner_id,
        current_user=_create_current_user(role=role),
    )


def _create_page() -> Page[DealShortDto]:
    return Page(
        items=[
            DealShortDto(
                id=1,
                contact_id=1,
                owner_id=1,
                title="Test Deal",
                amount=Decimal("1000"),
                currency="USD",
                status=DealStatuses.NEW,
                stage=DealStages.QUALIFICATION,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        ],
        page=1,
        page_size=20,
        total=1,
        pages=1,
    )


@pytest.mark.asyncio
async def test__execute__returns_page(
    use_case: GetDealsByCriteriaUseCase,
    deals_read_repo: AsyncMock,
) -> None:
    expected_page = _create_page()
    deals_read_repo.get_page_by_criteria.return_value = expected_page

    criteria = _create_criteria()
    result = await use_case.execute(criteria=criteria)

    assert result == expected_page
    deals_read_repo.get_page_by_criteria.assert_called_once()


@pytest.mark.asyncio
async def test__execute__admin_can_filter_by_owner(
    use_case: GetDealsByCriteriaUseCase,
    deals_read_repo: AsyncMock,
) -> None:
    deals_read_repo.get_page_by_criteria.return_value = _create_page()

    criteria = _create_criteria(owner_id=5, role=OrganizationMemberRoles.ADMIN)
    await use_case.execute(criteria=criteria)

    deals_read_repo.get_page_by_criteria.assert_called_once()


@pytest.mark.asyncio
async def test__execute__owner_can_filter_by_owner(
    use_case: GetDealsByCriteriaUseCase,
    deals_read_repo: AsyncMock,
) -> None:
    deals_read_repo.get_page_by_criteria.return_value = _create_page()

    criteria = _create_criteria(owner_id=5, role=OrganizationMemberRoles.OWNER)
    await use_case.execute(criteria=criteria)

    deals_read_repo.get_page_by_criteria.assert_called_once()


@pytest.mark.asyncio
async def test__execute__manager_can_filter_by_owner(
    use_case: GetDealsByCriteriaUseCase,
    deals_read_repo: AsyncMock,
) -> None:
    deals_read_repo.get_page_by_criteria.return_value = _create_page()

    criteria = _create_criteria(owner_id=5, role=OrganizationMemberRoles.MANAGER)
    await use_case.execute(criteria=criteria)

    deals_read_repo.get_page_by_criteria.assert_called_once()


@pytest.mark.asyncio
async def test__execute__member_cannot_filter_by_owner__raises_forbidden(
    use_case: GetDealsByCriteriaUseCase,
    deals_read_repo: AsyncMock,
) -> None:
    criteria = _create_criteria(owner_id=5, role=OrganizationMemberRoles.MEMBER)

    with pytest.raises(ForbiddenUserActionError):
        await use_case.execute(criteria=criteria)

    deals_read_repo.get_page_by_criteria.assert_not_called()


@pytest.mark.asyncio
async def test__execute__member_without_owner_filter__success(
    use_case: GetDealsByCriteriaUseCase,
    deals_read_repo: AsyncMock,
) -> None:
    deals_read_repo.get_page_by_criteria.return_value = _create_page()

    criteria = _create_criteria(owner_id=None, role=OrganizationMemberRoles.MEMBER)
    result = await use_case.execute(criteria=criteria)

    assert result is not None
    deals_read_repo.get_page_by_criteria.assert_called_once()
