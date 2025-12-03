from dataclasses import dataclass
from decimal import Decimal

from commons.entities import EntityId


@dataclass(kw_only=True)
class CreateDealDto:
    """Dto для создания сделки"""

    contact_id: EntityId
    title: str
    amount: Decimal
    currency: str
