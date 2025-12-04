from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from commons.datetime_utils import now_tz
from commons.entities import EntityId
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.errors import (
    DealStatusCannotBeWonWithZeroAmount,
    RollingBackDealStageIsProhibited,
)

DEAL_STAGES_ORDER = (
    DealStages.QUALIFICATION,
    DealStages.PROPOSAL,
    DealStages.NEGOTIATION,
    DealStages.CLOSED,
)
"""Порядок этапов сделки"""


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

    def set_status(self, status: DealStatuses) -> None:
        if status == DealStatuses.WON and self.amount == Decimal("0"):
            raise DealStatusCannotBeWonWithZeroAmount(id_=self.id)

        self.status = status
        self.updated_at = now_tz()

    def set_stage(self, stage: DealStages, skip_order_validation: bool = False) -> None:
        if not skip_order_validation:
            self._validate_change_stage_order(stage=stage)

        self.stage = stage
        self.updated_at = now_tz()

    def _validate_change_stage_order(self, stage: DealStages) -> None:
        new_stage_index = DEAL_STAGES_ORDER.index(stage)
        current_stage_index = DEAL_STAGES_ORDER.index(self.stage)

        if new_stage_index < current_stage_index:
            raise RollingBackDealStageIsProhibited(
                id_=self.id,
            )
