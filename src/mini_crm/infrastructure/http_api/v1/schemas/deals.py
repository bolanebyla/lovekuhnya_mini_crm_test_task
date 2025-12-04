from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from commons.http_api.schemas import PaginatedRequestSchema
from mini_crm.application.deals.dtos import (
    CreateDealDto,
    DealOrderBy,
    DealShortDto,
    GetDealsByCriteriaDto,
    OrderDirection,
    UpdateDealDto,
)
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class GetDealsByCriteriaSchema(PaginatedRequestSchema):
    """Схема критериев для получения списка сделок"""

    page: int = 1
    page_size: int = Field(20, le=100)

    status: list[DealStatuses] | None = Field(None, description="Фильтр по статусам")
    stage: DealStages | None = Field(None, description="Фильтр по стадии")
    min_amount: Decimal | None = Field(None, description="Минимальная сумма")
    max_amount: Decimal | None = Field(None, description="Максимальная сумма")
    owner_id: int | None = Field(None, description="Id владельца (для admin/owner)")

    order_by: DealOrderBy = Field(DealOrderBy.CREATED_AT, description="Поле сортировки")
    order: OrderDirection = Field(OrderDirection.DESC, description="Направление сортировки")

    def to_dto(self, current_user: OrganizationMemberDto) -> GetDealsByCriteriaDto:
        return GetDealsByCriteriaDto(
            page=self.page,
            page_size=self.page_size,
            statuses=self.status,
            stage=self.stage,
            min_amount=self.min_amount,
            max_amount=self.max_amount,
            owner_id=self.owner_id,
            order_by=self.order_by,
            order=self.order,
            current_user=current_user,
        )


class DealShortSchema(BaseModel):
    """Краткая информация по сделке"""

    id: int
    contact_id: int
    owner_id: int
    title: str
    amount: Decimal
    currency: str
    status: DealStatuses
    stage: DealStages
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_dto(cls, dto: DealShortDto) -> "DealShortSchema":
        return cls(
            id=dto.id,
            contact_id=dto.contact_id,
            owner_id=dto.owner_id,
            title=dto.title,
            amount=dto.amount,
            currency=dto.currency,
            status=dto.status,
            stage=dto.stage,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )


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
        return UpdateDealDto(
            deal_id=deal_id,
            status=self.status,
            stage=self.stage,
        )
