from unittest.mock import MagicMock

import pytest

from commons.app_errors.errors import EntityNotFoundByIdError, ForbiddenError
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.deals.services import DealsService
from tests.unit.application.deals.factories import create_deal
from tests.unit.factories import create_organization_member


@pytest.fixture(scope="function")
def service(deals_repo: DealsRepo) -> DealsService:
    return DealsService(deals_repo=deals_repo)


@pytest.mark.asyncio
async def test__get_deal_for_user__success(
    service: DealsService,
    deals_repo: MagicMock,
) -> None:
    deal = create_deal(organization_id=1)
    current_user = create_organization_member(organization_id=1)
    deals_repo.get_by_id.return_value = deal

    result = await service.get_deal_for_user(deal_id=1, current_user=current_user)

    assert result == deal
    deals_repo.get_by_id.assert_called_once_with(id_=1)


@pytest.mark.asyncio
async def test__get_deal_for_user__deal_not_found__raises_error(
    service: DealsService,
    deals_repo: MagicMock,
) -> None:
    current_user = create_organization_member(organization_id=1)
    deals_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundByIdError):
        await service.get_deal_for_user(deal_id=999, current_user=current_user)


@pytest.mark.asyncio
async def test__get_deal_for_user__wrong_organization__raises_forbidden(
    service: DealsService,
    deals_repo: MagicMock,
) -> None:
    deal = create_deal(organization_id=1)
    current_user = create_organization_member(organization_id=2)
    deals_repo.get_by_id.return_value = deal

    with pytest.raises(ForbiddenError):
        await service.get_deal_for_user(deal_id=1, current_user=current_user)


@pytest.mark.asyncio
async def test__check_deal_access__success(
    service: DealsService,
    deals_repo: MagicMock,
) -> None:
    deal = create_deal(organization_id=1)
    current_user = create_organization_member(organization_id=1)
    deals_repo.get_by_id.return_value = deal

    await service.check_deal_access(deal_id=1, current_user=current_user)

    deals_repo.get_by_id.assert_called_once_with(id_=1)


@pytest.mark.asyncio
async def test__check_deal_access__deal_not_found__raises_error(
    service: DealsService,
    deals_repo: MagicMock,
) -> None:
    current_user = create_organization_member(organization_id=1)
    deals_repo.get_by_id.return_value = None

    with pytest.raises(EntityNotFoundByIdError):
        await service.check_deal_access(deal_id=999, current_user=current_user)


@pytest.mark.asyncio
async def test__check_deal_access__wrong_organization__raises_forbidden(
    service: DealsService,
    deals_repo: MagicMock,
) -> None:
    deal = create_deal(organization_id=1)
    current_user = create_organization_member(organization_id=2)
    deals_repo.get_by_id.return_value = deal

    with pytest.raises(ForbiddenError):
        await service.check_deal_access(deal_id=1, current_user=current_user)
