from datetime import date, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient

from mini_crm.application.tasks.dtos import TaskShortDto
from mini_crm.application.tasks.use_cases import CreateTaskUseCase, GetTasksByCriteriaUseCase


@pytest.fixture
def use_case_mocks() -> dict[type, MagicMock]:
    get_tasks_mock = AsyncMock()
    get_tasks_mock.execute = AsyncMock(
        return_value=[
            TaskShortDto(
                id=1,
                deal_id=1,
                title="Test Task",
                description="Test Description",
                due_date=date.today(),
                is_done=False,
                created_at=datetime.now(),
            )
        ]
    )

    create_task_mock = AsyncMock()
    create_task_mock.execute = AsyncMock(return_value=None)

    return {
        GetTasksByCriteriaUseCase: get_tasks_mock,
        CreateTaskUseCase: create_task_mock,
    }


@pytest.mark.asyncio
async def test__get_tasks__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get("/api/v1/tasks/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Task"


@pytest.mark.asyncio
async def test__get_tasks__with_filters(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.get(
        "/api/v1/tasks/",
        params={
            "deal_id": 1,
            "only_open": True,
        },
    )

    assert response.status_code == 200
    use_case_mocks[GetTasksByCriteriaUseCase].execute.assert_called_once()


@pytest.mark.asyncio
async def test__create_task__success(
    client: AsyncClient,
    use_case_mocks: dict[type, MagicMock],
) -> None:
    response = await client.post(
        "/api/v1/tasks/",
        json={
            "deal_id": 1,
            "title": "New Task",
            "description": "Task Description",
            "due_date": str(date.today()),
        },
    )

    assert response.status_code == 200
    use_case_mocks[CreateTaskUseCase].execute.assert_called_once()
