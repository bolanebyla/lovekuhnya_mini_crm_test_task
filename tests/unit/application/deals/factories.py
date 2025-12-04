from datetime import UTC, datetime
from decimal import Decimal

from mini_crm.application.deals.dtos import UpdateDealDto
from mini_crm.application.deals.entities import Deal
from mini_crm.application.deals.enums import DealStages, DealStatuses


def create_deal(
    id_: int = 1,
    organization_id: int = 1,
    owner_id: int = 1,
    amount: Decimal = Decimal("1000"),
    status: DealStatuses = DealStatuses.NEW,
    stage: DealStages = DealStages.QUALIFICATION,
    created_at: datetime | None = None,
    updated_at: datetime | None = None,
) -> Deal:
    now = datetime(day=1, month=12, year=2025, tzinfo=UTC)
    return Deal(
        id=id_,
        organization_id=organization_id,
        contact_id=1,
        owner_id=owner_id,
        title="Test Deal",
        amount=amount,
        currency="USD",
        status=status,
        stage=stage,
        created_at=created_at or now,
        updated_at=updated_at or now,
    )


def create_update_deal_dto(
    deal_id: int = 1,
    status: DealStatuses = DealStatuses.IN_PROGRESS,
    stage: DealStages = DealStages.QUALIFICATION,
) -> UpdateDealDto:
    return UpdateDealDto(
        deal_id=deal_id,
        status=status,
        stage=stage,
    )
