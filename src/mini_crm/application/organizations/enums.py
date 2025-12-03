from enum import StrEnum


class OrganizationMemberRoles(StrEnum):
    """Роли члена организации"""

    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
