from unittest.mock import MagicMock

import pytest

from mini_crm.application.activities.entities import Activity
from mini_crm.application.activities.enums import ActivityTypes
from mini_crm.application.activities.interfaces import ActivitiesRepo
from mini_crm.application.activities.services import ActivitiesService


@pytest.fixture(scope="function")
def service(activities_repo: ActivitiesRepo) -> ActivitiesService:
    return ActivitiesService(activities_repo=activities_repo)


@pytest.mark.asyncio
async def test__create_activity__success(
    service: ActivitiesService,
    activities_repo: MagicMock,
) -> None:
    await service.create_activity(
        deal_id=1,
        type_=ActivityTypes.COMMENT,
        payload={"text": "Test comment"},
        author_id=1,
    )

    activities_repo.add.assert_called_once()
    activity: Activity = activities_repo.add.call_args.kwargs["activity"]
    assert activity.deal_id == 1
    assert activity.type == ActivityTypes.COMMENT
    assert activity.payload == {"text": "Test comment"}
    assert activity.author_id == 1


@pytest.mark.asyncio
async def test__create_activity__without_author__success(
    service: ActivitiesService,
    activities_repo: MagicMock,
) -> None:
    await service.create_activity(
        deal_id=1,
        type_=ActivityTypes.SYSTEM,
        payload={"event": "system_event"},
    )

    activities_repo.add.assert_called_once()
    activity: Activity = activities_repo.add.call_args.kwargs["activity"]
    assert activity.author_id is None


@pytest.mark.asyncio
async def test__create_status_changed_activity__success(
    service: ActivitiesService,
    activities_repo: MagicMock,
) -> None:
    await service.create_status_changed_activity(
        deal_id=1,
        old_status="new",
        new_status="won",
    )

    activities_repo.add.assert_called_once()
    activity: Activity = activities_repo.add.call_args.kwargs["activity"]
    assert activity.deal_id == 1
    assert activity.type == ActivityTypes.STATUS_CHANGED
    assert activity.payload == {"old_status": "new", "new_status": "won"}
    assert activity.author_id is None


@pytest.mark.asyncio
async def test__create_stage_changed_activity__success(
    service: ActivitiesService,
    activities_repo: MagicMock,
) -> None:
    await service.create_stage_changed_activity(
        deal_id=1,
        old_stage="qualification",
        new_stage="proposal",
    )

    activities_repo.add.assert_called_once()
    activity: Activity = activities_repo.add.call_args.kwargs["activity"]
    assert activity.deal_id == 1
    assert activity.type == ActivityTypes.STAGE_CHANGED
    assert activity.payload == {"old_stage": "qualification", "new_stage": "proposal"}
