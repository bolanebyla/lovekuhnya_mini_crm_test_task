from pydantic import BaseModel

from mini_crm.application.organizations.dtos import UserOrganizationDto


class UserOrganizationSchema(BaseModel):
    """Организация пользователя"""

    id: int
    name: str

    @classmethod
    def from_dto(cls, dto: UserOrganizationDto) -> "UserOrganizationSchema":
        return cls(
            id=dto.id,
            name=dto.name,
        )
