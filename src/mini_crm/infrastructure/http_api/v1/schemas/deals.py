from decimal import Decimal

from pydantic import BaseModel

from mini_crm.application.deals.dtos import CreateDealDto, UpdateDealDto
from mini_crm.application.deals.enums import DealStages, DealStatuses


class CreateDealSchema(BaseModel):
    """Схема создания сделки"""

    contact_id: int
    title: str
    amount: Decimal
    currency: str

    def to_dto(self) -> CreateDealDto:
        return CreateDealDto(
            contact_id=self.contact_id,
            title=self.title,
            amount=self.amount,
            currency=self.currency,
        )


class UpdateDealSchema(BaseModel):
    """Схема обновления сделки"""

    status: DealStatuses
    stage: DealStages

    def to_dto(self, deal_id: int) -> UpdateDealDto:
        return UpdateDealDto(deal_id=deal_id, status=self.status, stage=self.stage)
