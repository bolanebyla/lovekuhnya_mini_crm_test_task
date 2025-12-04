from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from mini_crm.application.activities.dtos import ActivityDto
from mini_crm.application.activities.enums import ActivityTypes
from mini_crm.application.activities.use_cases import (
    CreateManualDealActivityUseCase,
    GetActivitiesByDealUseCase,
)


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    get_activities_mock = AsyncMock()
    get_activities_mock.execute = AsyncMock(
        return_value=[
            ActivityDto(
                id=1,
                deal_id=1,
                author_id=1,
                type=ActivityTypes.COMMENT,
                payload={"text": "Test comment"},
                created_at=datetime.now(),
            )
        ]
    )

    create_activity_mock = AsyncMock()
    create_activity_mock.execute = AsyncMock(return_value=None)

    return {
        GetActivitiesByDealUseCase: get_activities_mock,
        CreateManualDealActivityUseCase: create_activity_mock,
    }


@pytest.mark.asyncio
async def test__get_activities_by_deal__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get("/api/v1/deals/1/activities/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["type"] == "comment"


@pytest.mark.asyncio
async def test__create_activity__comment__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/deals/1/activities/",
        json={
            "type": "comment",
            "payload": {"text": "New comment"},
        },
    )

    assert response.status_code == 200
    use_case_mocks[CreateManualDealActivityUseCase].execute.assert_called_once()
