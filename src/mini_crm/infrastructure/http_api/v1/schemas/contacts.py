from pydantic import BaseModel, Field

from commons.http_api.schemas import PaginatedRequestSchema
from mini_crm.application.contacts.dtos import ContactShortDto, GetContactsByCriteriaDto
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class GetContactsByCriteriaSchema(PaginatedRequestSchema):
    """Схема критериев для получения списка контактов"""

    page: int = 1
    page_size: int = Field(..., le=100)

    search: str | None = Field(None, description="Поиск по name/email")
    owner_id: int | None = Field(None, description="Id пользователя владельца контакта")

    def to_dto(self, current_user: OrganizationMemberDto) -> GetContactsByCriteriaDto:
        return GetContactsByCriteriaDto(
            page=self.page,
            page_size=self.page_size,
            search=self.search,
            owner_id=self.owner_id,
            current_user=current_user,
        )


class ContactShortSchema(BaseModel):
    """Краткая информация по контакту"""

    id: int
    name: str
    email: str
    phone: str

    @classmethod
    def from_dto(cls, dto: ContactShortDto) -> "ContactShortSchema":
        return cls(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            phone=dto.phone,
        )
