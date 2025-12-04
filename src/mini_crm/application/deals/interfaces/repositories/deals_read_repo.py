from typing import Protocol

from commons.dtos.pagination import Page
from mini_crm.application.deals.dtos import DealShortDto, GetDealsByCriteriaDto


class DealsReadRepo(Protocol):
    """Репозиторий для чтения сделок"""

    async def get_page_by_criteria(
        self,
        criteria: GetDealsByCriteriaDto,
    ) -> Page[DealShortDto]: ...
