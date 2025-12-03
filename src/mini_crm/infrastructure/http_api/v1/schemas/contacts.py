from pydantic import BaseModel, Field

from commons.http_api.schemas import PaginatedRequestSchema
from mini_crm.application.contacts.dtos import ContactShortDto, GetContactsByCriteriaDto
from mini_crm.infrastructure.http_api.auth import CurrentUser


class GetContactsByCriteriaSchema(PaginatedRequestSchema):
    """Схема критериев для получения списка контактов"""

    page: int = 1
    page_size: int = Field(..., le=100)

    search: str | None = Field(None, description="Поиск по name/email")
    owner_id: int | None = Field(None, description="Id пользователя владельца контакта")

    def to_dto(self, current_user: CurrentUser) -> GetContactsByCriteriaDto:
        return GetContactsByCriteriaDto(
            page=self.page,
            page_size=self.page_size,
            search=self.search,
            owner_id=self.owner_id,
            organization_id=current_user.organization_id,
            current_user_id=current_user.user_id,
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
