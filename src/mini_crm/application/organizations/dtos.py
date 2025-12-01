from dataclasses import dataclass

from commons.entities import EntityId


@dataclass
class UserOrganisationDto:
    """Организация пользователя"""

    id: EntityId
    name: str
