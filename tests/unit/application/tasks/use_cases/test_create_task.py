from datetime import date, timedelta
from typing import cast
from unittest.mock import MagicMock, create_autospec

import pytest

from commons.app_errors.errors import ForbiddenError
from commons.operations import AsyncOperation
from mini_crm.application.deals.services import DealsService
from mini_crm.application.organizations.enums import OrganizationMemberRoles
from mini_crm.application.tasks.errors import TaskDueDateInPastError
from mini_crm.application.tasks.interfaces import TasksRepo
from mini_crm.application.tasks.use_cases import CreateTaskUseCase
from tests.unit.application.deals.factories import create_deal
from tests.unit.application.tasks.factories import create_task_dto
from tests.unit.factories import create_organization_member


@pytest.fixture(scope="function")
def deals_service() -> MagicMock:
    return cast(MagicMock, create_autospec(DealsService, spec_set=True, instance=True))


@pytest.fixture(scope="function")
def use_case(
    operation: AsyncOperation,
    tasks_repo: TasksRepo,
    deals_service: MagicMock,
) -> CreateTaskUseCase:
    return CreateTaskUseCase(
        operation=operation,
        tasks_repo=tasks_repo,
        deals_service=deals_service,
    )


@pytest.mark.asyncio
async def test__create_task__success(
    use_case: CreateTaskUseCase,
    tasks_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(owner_id=1)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_task_dto()
    current_user = create_organization_member(user_id=1, role=OrganizationMemberRoles.MEMBER)

    await use_case.execute(create_dto=dto, current_user=current_user)

    tasks_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__create_task__due_date_in_past__raises_error(
    use_case: CreateTaskUseCase,
) -> None:
    dto = create_task_dto(due_date=date.today() - timedelta(days=1))
    current_user = create_organization_member()

    with pytest.raises(TaskDueDateInPastError):
        await use_case.execute(create_dto=dto, current_user=current_user)


@pytest.mark.asyncio
async def test__create_task__member_for_own_deal__success(
    use_case: CreateTaskUseCase,
    tasks_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(owner_id=1)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_task_dto()
    current_user = create_organization_member(user_id=1, role=OrganizationMemberRoles.MEMBER)

    await use_case.execute(create_dto=dto, current_user=current_user)

    tasks_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__create_task__member_for_other_user_deal__raises_forbidden(
    use_case: CreateTaskUseCase,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(owner_id=2)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_task_dto()
    current_user = create_organization_member(user_id=1, role=OrganizationMemberRoles.MEMBER)

    with pytest.raises(ForbiddenError):
        await use_case.execute(create_dto=dto, current_user=current_user)


@pytest.mark.asyncio
async def test__create_task__manager_for_any_deal__success(
    use_case: CreateTaskUseCase,
    tasks_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(owner_id=999)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_task_dto()
    current_user = create_organization_member(user_id=1, role=OrganizationMemberRoles.MANAGER)

    await use_case.execute(create_dto=dto, current_user=current_user)

    tasks_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__create_task__admin_for_any_deal__success(
    use_case: CreateTaskUseCase,
    tasks_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(owner_id=999)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_task_dto()
    current_user = create_organization_member(user_id=1, role=OrganizationMemberRoles.ADMIN)

    await use_case.execute(create_dto=dto, current_user=current_user)

    tasks_repo.add.assert_called_once()


@pytest.mark.asyncio
async def test__create_task__owner_for_any_deal__success(
    use_case: CreateTaskUseCase,
    tasks_repo: MagicMock,
    deals_service: MagicMock,
) -> None:
    deal = create_deal(owner_id=999)
    deals_service.get_deal_for_user.return_value = deal
    dto = create_task_dto()
    current_user = create_organization_member(user_id=1, role=OrganizationMemberRoles.OWNER)

    await use_case.execute(create_dto=dto, current_user=current_user)

    tasks_repo.add.assert_called_once()
