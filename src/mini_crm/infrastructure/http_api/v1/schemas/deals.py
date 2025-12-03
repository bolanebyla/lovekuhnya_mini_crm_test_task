from decimal import Decimal

from pydantic import BaseModel

from mini_crm.application.deals.dtos import CreateDealDto


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
