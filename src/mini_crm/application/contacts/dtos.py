from dataclasses import dataclass

from commons.dtos.pagination import PaginatedRequestDto
from commons.entities import EntityId


@dataclass(kw_only=True)
class GetContactsByCriteriaDto(PaginatedRequestDto):
    """Критерии для получения контактов"""

    search: str | None = None
    owner_id: EntityId | None = None
    """Id пользователя владельца контакта"""

    organization_id: EntityId
    current_user_id: EntityId
    """Id текущего пользователя"""


@dataclass(kw_only=True)
class ContactShortDto:
    """Краткая информация по контакту"""

    id: EntityId
    name: str
    email: str
    phone: str
