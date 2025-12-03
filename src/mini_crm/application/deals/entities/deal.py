from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from commons.entities import EntityId
from mini_crm.application.deals.enums import DealStages, DealStatuses


@dataclass(kw_only=True)
class Deal:
    """Сделка"""

    id: EntityId | None = None

    organization_id: EntityId
    contact_id: EntityId
    owner_id: EntityId

    title: str
    amount: Decimal
    currency: str
    status: DealStatuses
    stage: DealStages
    """Этап воронки"""

    created_at: datetime
    updated_at: datetime
