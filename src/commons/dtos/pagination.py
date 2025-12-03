from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(kw_only=True)
class PaginatedRequestDto:
    """Запрос на получение объектов с пагинацией"""

    page: int = 1
    page_size: int


@dataclass(kw_only=True)
class Page[T]:
    """Страница пагинации"""

    items: list[T]
    page: int
    page_size: int
    total: int
    pages: int
