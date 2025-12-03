import pytest

from commons.operations import AsyncOperation
from mini_crm.application.organizations.dtos import UserOrganisationDto
from mini_crm.application.organizations.interfaces import OrganizationsReadRepo
from mini_crm.application.organizations.use_cases import GetUserOrganisationsUseCase


@pytest.fixture(scope="function")
def use_case(
    operation: AsyncOperation,
    organizations_read_repo: OrganizationsReadRepo,
) -> GetUserOrganisationsUseCase:
    return GetUserOrganisationsUseCase(
        operation=operation,
        organizations_read_repo=organizations_read_repo,
    )


@pytest.mark.asyncio
async def test__get_user_organisations__list(
    use_case: GetUserOrganisationsUseCase,
    organizations_read_repo: OrganizationsReadRepo,
) -> None:
    expected = [
        UserOrganisationDto(
            id=1,
            name="test 1",
        ),
        UserOrganisationDto(
            id=1,
            name="test 2",
        ),
    ]

    organizations_read_repo.get_list_by_member_user_id.return_value = expected  # type: ignore[attr-defined]

    result = await use_case.execute(user_id=1)

    assert isinstance(result, list)
    assert result == expected


@pytest.mark.asyncio
async def test__get_user_organisations__empty(
    use_case: GetUserOrganisationsUseCase,
    organizations_read_repo: OrganizationsReadRepo,
) -> None:
    organizations_read_repo.get_list_by_member_user_id.return_value = []  # type: ignore[attr-defined]

    result = await use_case.execute(user_id=1)

    assert isinstance(result, list)
    assert result == []
