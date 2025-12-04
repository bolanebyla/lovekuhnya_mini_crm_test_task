from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from commons.operations import AsyncOperation
from mini_crm.application.activities.enums import ActivityTypes
from mini_crm.application.activities.errors import OnlyCommentActivityTypeAllowedError
from mini_crm.application.activities.services import ActivitiesService
from mini_crm.application.activities.use_cases import CreateManualDealActivityUseCase
from mini_crm.application.deals.services import DealsService
from tests.unit.application.activities.factories import create_activity_dto
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
    activities_service: MagicMock,
    deals_service: MagicMock,
) -> CreateManualDealActivityUseCase:
    return CreateManualDealActivityUseCase(
        operation=operation,
        activities_service=activities_service,
        deals_service=deals_service,
    )


@pytest.mark.asyncio
async def test__create_manual_activity__comment__success(
    use_case: CreateManualDealActivityUseCase,
    activities_service: MagicMock,
    deals_service: MagicMock,
) -> None:
    dto = create_activity_dto(type_=ActivityTypes.COMMENT)
    current_user = create_organization_member()

    await use_case.execute(deal_id=1, create_dto=dto, current_user=current_user)

    deals_service.check_deal_access.assert_called_once()
    activities_service.create_activity.assert_called_once_with(
        deal_id=1,
        type_=ActivityTypes.COMMENT,
        payload={"text": "Test comment"},
        author_id=1,
    )


@pytest.mark.asyncio
async def test__create_manual_activity__status_changed__raises_error(
    use_case: CreateManualDealActivityUseCase,
) -> None:
    dto = create_activity_dto(type_=ActivityTypes.STATUS_CHANGED)
    current_user = create_organization_member()

    with pytest.raises(OnlyCommentActivityTypeAllowedError):
        await use_case.execute(deal_id=1, create_dto=dto, current_user=current_user)


@pytest.mark.asyncio
async def test__create_manual_activity__system__raises_error(
    use_case: CreateManualDealActivityUseCase,
) -> None:
    dto = create_activity_dto(type_=ActivityTypes.SYSTEM)
    current_user = create_organization_member()

    with pytest.raises(OnlyCommentActivityTypeAllowedError):
        await use_case.execute(deal_id=1, create_dto=dto, current_user=current_user)
