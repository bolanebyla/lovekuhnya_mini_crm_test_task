from dataclasses import dataclass
from decimal import Decimal

from commons.entities import EntityId
from mini_crm.application.deals.enums import DealStages, DealStatuses


@dataclass(kw_only=True)
class CreateDealDto:
    """Dto для создания сделки"""

    contact_id: EntityId
    title: str
    amount: Decimal
    currency: str


@dataclass(kw_only=True)
class UpdateDealDto:
    """Dto для обновления сделки"""

    id: EntityId
    status: DealStatuses
    stage: DealStages
