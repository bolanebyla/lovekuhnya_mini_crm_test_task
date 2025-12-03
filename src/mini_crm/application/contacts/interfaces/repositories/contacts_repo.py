from abc import abstractmethod
from typing import Protocol

from mini_crm.application.contacts.entities import Contact


class ContactsRepo(Protocol):
    """Репозитория для контактов"""

    @abstractmethod
    async def add(self, contact: Contact) -> None:
        """Добавляет контакт в хранилище"""
        ...
