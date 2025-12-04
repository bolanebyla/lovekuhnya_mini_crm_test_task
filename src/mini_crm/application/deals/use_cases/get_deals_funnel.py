from decimal import Decimal

from commons.operations import AsyncOperation, async_operation
from mini_crm.application.deals.dtos import (
    DealsFunnelDto,
    DealStageConversionDto,
    DealStageFunnelItemDto,
)
from mini_crm.application.deals.entities import DEAL_STAGES_ORDER
from mini_crm.application.deals.enums import DealStages, DealStatuses
from mini_crm.application.deals.interfaces import DealsAnalyticsRepo
from mini_crm.application.organizations.dtos import OrganizationMemberDto


class GetDealsFunnelUseCase:
    """Получить воронку продаж"""

    def __init__(
        self,
        operation: AsyncOperation,
        deals_analytics_repo: DealsAnalyticsRepo,
    ):
        self._operation = operation
        self._deals_analytics_repo = deals_analytics_repo

    @async_operation
    async def execute(
        self,
        current_user: OrganizationMemberDto,
    ) -> DealsFunnelDto:
        organization_id = current_user.organization_id

        by_stage_and_status = await self._deals_analytics_repo.get_funnel_by_stage_and_status(
            organization_id=organization_id,
        )

        by_stage_and_status = self._fill_all_stages_and_statuses(by_stage_and_status)

        stage_totals = self._calculate_stage_totals(by_stage_and_status)

        conversions = self._calculate_conversions(stage_totals)

        return DealsFunnelDto(
            by_stage_and_status=by_stage_and_status,
            conversions=conversions,
        )

    def _fill_all_stages_and_statuses(
        self,
        by_stage_and_status: list[DealStageFunnelItemDto],
    ) -> list[DealStageFunnelItemDto]:
        """Заполняет данные по всем стадиям и статусам, даже если данных нет"""
        existing = {(item.stage, item.status): item for item in by_stage_and_status}

        result = []
        for stage in DealStages:
            for status in DealStatuses:
                item = existing.get(
                    (stage, status),
                    DealStageFunnelItemDto(stage=stage, status=status, count=0),
                )
                result.append(item)

        return result

    def _calculate_stage_totals(
        self,
        by_stage_and_status: list[DealStageFunnelItemDto],
    ) -> dict[DealStages, int]:
        """Считает общее количество сделок по каждой стадии"""
        totals: dict[DealStages, int] = {stage: 0 for stage in DealStages}

        for item in by_stage_and_status:
            totals[item.stage] += item.count

        return totals

    def _calculate_conversions(
        self,
        stage_totals: dict[DealStages, int],
    ) -> list[DealStageConversionDto]:
        """Рассчитывает конверсию между стадиями"""
        conversions = []

        for i in range(len(DEAL_STAGES_ORDER) - 1):
            from_stage = DEAL_STAGES_ORDER[i]
            to_stage = DEAL_STAGES_ORDER[i + 1]

            from_count = stage_totals.get(from_stage, 0)
            to_count = stage_totals.get(to_stage, 0)

            if from_count > 0:
                conversion_percent = Decimal(to_count) / Decimal(from_count) * 100
            else:
                conversion_percent = Decimal("0")

            conversions.append(
                DealStageConversionDto(
                    from_stage=from_stage,
                    to_stage=to_stage,
                    conversion_percent=conversion_percent.quantize(Decimal("0.01")),
                )
            )

        return conversions
