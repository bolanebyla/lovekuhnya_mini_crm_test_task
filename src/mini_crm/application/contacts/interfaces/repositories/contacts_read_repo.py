from abc import abstractmethod
from typing import Protocol

from commons.dtos.pagination import Page
from mini_crm.application.contacts.dtos import ContactShortDto, GetContactsByCriteriaDto


class ContactsReadRepo(Protocol):
    """Репозитория для чтения контактов"""

    @abstractmethod
    async def get_page_by_criteria(
        self,
        criteria: GetContactsByCriteriaDto,
    ) -> Page[ContactShortDto]:
        """Получает список контактов по критериям"""
        ...
