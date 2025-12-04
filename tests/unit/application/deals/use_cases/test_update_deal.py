from decimal import Decimal
from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from commons.operations import AsyncOperation
from mini_crm.application.activities.services import ActivitiesService
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.errors import (
    DealStatusCannotBeWonWithZeroAmount,
    RollingBackDealStageIsProhibited,
)
from mini_crm.application.deals.interfaces import DealsRepo
from mini_crm.application.deals.services import DealsService
from mini_crm.application.deals.use_cases.update_deal import UpdateDealUseCase
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from tests.unit.application.deals.factories import create_deal, create_update_deal_dto
from tests.unit.factories import create_organization_member


@pytest.fixture(scope="function")
def deals_service() -> MagicMock:
    return cast(MagicMock, create_autospec(DealsService, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def activities_service() -> MagicMock:
    return cast(MagicMock, create_autospec(ActivitiesService, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def use_case(
    operation: AsyncOperation,
    deals_repo: DealsRepo,
    deals_service: MagicMock,
    activities_service: MagicMock,
) -> UpdateDealUseCase:
    return UpdateDealUseCase(
        operation=operation,
        deals_repo=deals_repo,
        deals_service=deals_service,
        activities_service=activities_service,
    )


@pytest.mark.asyncio
async def test__update_deal__success(
    use_case: UpdateDealUseCase,
    deals_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal()
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(status=DealStatuses.IN_PROGRESS, stage=DealStages.PROPOSAL)
    current_user = create_organization_member()

    await use_case.execute(update_dto=dto, current_user=current_user)

    deals_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__update_deal__status_to_won_with_zero_amount__raises_error(
    use_case: UpdateDealUseCase,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(amount=Decimal("0"), status=DealStatuses.IN_PROGRESS)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(status=DealStatuses.WON)
    current_user = create_organization_member()

    with pytest.raises(DealStatusCannotBeWonWithZeroAmount):
        await use_case.execute(update_dto=dto, current_user=current_user)


@pytest.mark.asyncio
async def test__update_deal__member_rollback_stage__raises_error(
    use_case: UpdateDealUseCase,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(stage=DealStages.NEGOTIATION)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(stage=DealStages.QUALIFICATION)
    current_user = create_organization_member(role=OrganizationMemberRoles.MEMBER)

    with pytest.raises(RollingBackDealStageIsProhibited):
        await use_case.execute(update_dto=dto, current_user=current_user)


@pytest.mark.asyncio
async def test__update_deal__admin_rollback_stage__success(
    use_case: UpdateDealUseCase,
    deals_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(stage=DealStages.NEGOTIATION)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(stage=DealStages.QUALIFICATION)
    current_user = create_organization_member(role=OrganizationMemberRoles.ADMIN)

    await use_case.execute(update_dto=dto, current_user=current_user)

    deals_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__update_deal__owner_rollback_stage__success(
    use_case: UpdateDealUseCase,
    deals_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(stage=DealStages.NEGOTIATION)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(stage=DealStages.QUALIFICATION)
    current_user = create_organization_member(role=OrganizationMemberRoles.OWNER)

    await use_case.execute(update_dto=dto, current_user=current_user)

    deals_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__update_deal__status_changed__creates_activity(
    use_case: UpdateDealUseCase,
    deals_repo: MagicMock,
    deals_service: MagicMock,
    activities_service: MagicMock,
) -> None:
    deal = create_deal(status=DealStatuses.NEW)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(status=DealStatuses.WON, stage=DealStages.QUALIFICATION)
    current_user = create_organization_member()

    await use_case.execute(update_dto=dto, current_user=current_user)

    activities_service.create_status_changed_activity.assert_called_once_with(
        deal_id=1,
        old_status=DealStatuses.NEW,
        new_status=DealStatuses.WON,
    )


@pytest.mark.asyncio
async def test__update_deal__stage_changed__creates_activity(
    use_case: UpdateDealUseCase,
    deals_repo: MagicMock,
    deals_service: MagicMock,
    activities_service: MagicMock,
) -> None:
    deal = create_deal(stage=DealStages.QUALIFICATION)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(stage=DealStages.PROPOSAL)
    current_user = create_organization_member()

    await use_case.execute(update_dto=dto, current_user=current_user)

    activities_service.create_stage_changed_activity.assert_called_once_with(
        deal_id=1,
        old_stage=DealStages.QUALIFICATION,
        new_stage=DealStages.PROPOSAL,
    )


@pytest.mark.asyncio
async def test__update_deal__no_changes__no_activity_created(
    use_case: UpdateDealUseCase,
    deals_repo: MagicMock,
    deals_service: MagicMock,
    activities_service: MagicMock,
) -> None:
    deal = create_deal(status=DealStatuses.NEW, stage=DealStages.QUALIFICATION)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_update_deal_dto(status=DealStatuses.NEW, stage=DealStages.QUALIFICATION)
    current_user = create_organization_member()

    await use_case.execute(update_dto=dto, current_user=current_user)

    activities_service.create_status_changed_activity.assert_not_called()
    activities_service.create_stage_changed_activity.assert_not_called()
