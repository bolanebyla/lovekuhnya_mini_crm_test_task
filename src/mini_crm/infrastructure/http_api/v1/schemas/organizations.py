from pydantic import BaseModel

from mini_crm.application.organizations.dtos import UserOrganisationDto


class UserOrganisationSchema(BaseModel):
    """Организация пользователя"""

    id: int
    name: str

    @classmethod
    def from_dto(cls, dto: UserOrganisationDto) -> "UserOrganisationSchema":
        return cls(
            id=dto.id,
            name=dto.name,
        )
