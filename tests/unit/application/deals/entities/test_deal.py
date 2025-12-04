from decimal import Decimal

import pytest

from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.errors import (
    DealStatusCannotBeWonWithZeroAmount,
    RollingBackDealStageIsProhibited,
)
from tests.unit.application.deals.factories import create_deal


def test__set_status__success() -> None:
    deal = create_deal(status=DealStatuses.NEW)
    old_updated_at = deal.updated_at

    deal.set_status(DealStatuses.IN_PROGRESS)

    assert deal.status == DealStatuses.IN_PROGRESS
    assert deal.updated_at > old_updated_at


def test__set_status__won_with_positive_amount__success() -> None:
    deal = create_deal(amount=Decimal("1000"), status=DealStatuses.IN_PROGRESS)

    deal.set_status(DealStatuses.WON)

    assert deal.status == DealStatuses.WON


def test__set_status__won_with_zero_amount__raises_error() -> None:
    deal = create_deal(amount=Decimal("0"), status=DealStatuses.IN_PROGRESS)

    with pytest.raises(DealStatusCannotBeWonWithZeroAmount):
        deal.set_status(DealStatuses.WON)


def test__set_stage__forward__success() -> None:
    deal = create_deal(stage=DealStages.QUALIFICATION)
    old_updated_at = deal.updated_at

    deal.set_stage(DealStages.PROPOSAL)

    assert deal.stage == DealStages.PROPOSAL
    assert deal.updated_at > old_updated_at


def test__set_stage__same_stage__success() -> None:
    deal = create_deal(stage=DealStages.PROPOSAL)

    deal.set_stage(DealStages.PROPOSAL)

    assert deal.stage == DealStages.PROPOSAL


def test__set_stage__backward__raises_error() -> None:
    deal = create_deal(stage=DealStages.NEGOTIATION)

    with pytest.raises(RollingBackDealStageIsProhibited):
        deal.set_stage(DealStages.QUALIFICATION)


def test__set_stage__backward_with_skip_validation__success() -> None:
    deal = create_deal(stage=DealStages.NEGOTIATION)

    deal.set_stage(DealStages.QUALIFICATION, skip_order_validation=True)

    assert deal.stage == DealStages.QUALIFICATION
