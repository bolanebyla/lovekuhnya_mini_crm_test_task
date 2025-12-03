from enum import StrEnum


class OrganizationMemberRoles(StrEnum):
    """Роли участников организации"""

    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
