from abc import abstractmethod
from typing import Protocol

from mini_crm.application.users.entities import User


class UsersRepo(Protocol):
    """Репозиторий для пользователей"""

    @abstractmethod
    async def add(self, user: User) -> None:
        """Добавляет пользователя в хранилище"""
        ...

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Получает пользователя по email"""
        ...
