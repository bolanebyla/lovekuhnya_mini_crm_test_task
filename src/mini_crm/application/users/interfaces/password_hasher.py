from abc import abstractmethod
from typing import Protocol


class PasswordHasher(Protocol):
    """Хеширование паролей"""

    @abstractmethod
    def hash(self, password: str) -> str:
        """Хеширует пароль"""
        ...

    @abstractmethod
    def verify(self, password: str, hashed_password: str) -> bool:
        """Проверяет пароль"""
        ...
