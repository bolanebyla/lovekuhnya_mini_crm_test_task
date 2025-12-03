from abc import abstractmethod
from typing import Protocol

from commons.entities import EntityId
from mini_crm.application.contacts.entities import Contact


class ContactsRepo(Protocol):
    """Репозитория для контактов"""

    @abstractmethod
    async def add(self, contact: Contact) -> None:
        """Добавляет контакт в хранилище"""
        ...

    @abstractmethod
    async def get_by_id(self, id_: EntityId) -> Contact | None:
        """Получает по id"""
        ...
