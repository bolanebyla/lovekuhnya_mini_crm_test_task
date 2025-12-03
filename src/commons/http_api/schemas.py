from typing import TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedRequestSchema(BaseModel):
    """Схема запроса на получение объектов с пагинацией"""

    page: int = Field(1, gt=0)
    page_size: int = Field(..., le=100)


class PageSchema[T](BaseModel):
    """Схема страницы пагинации"""

    items: list[T]
    page: int
    page_size: int
    total: int
    pages: int
