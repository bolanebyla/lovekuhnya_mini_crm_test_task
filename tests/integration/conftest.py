import pytest

from mini_crm.application.organizations.dtos import OrganizationMemberDto
from mini_crm.application.organizations.enums import OrganizationMemberRoles


@pytest.fixture(scope="function")
def mock_current_user() -> OrganizationMemberDto:
    """Мок текущего пользователя"""
    return OrganizationMemberDto(
        user_id=1,
        organization_id=1,
        role=OrganizationMemberRoles.OWNER,
    )


@pytest.fixture(scope="function")
def mock_current_user_member() -> OrganizationMemberDto:
    """Мок текущего пользователя с ролью member"""
    return OrganizationMemberDto(
        user_id=2,
        organization_id=1,
        role=OrganizationMemberRoles.MEMBER,
    )
