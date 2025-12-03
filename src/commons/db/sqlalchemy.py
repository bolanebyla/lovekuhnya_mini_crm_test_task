from contextlib import AbstractAsyncContextManager
from contextvars import ContextVar
from math import ceil
from types import TracebackType
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from commons.dtos.pagination import PaginatedRequestDto


class BaseTransactionContextException(Exception):
    """
    Базовый класс контекстного менеджера транзакций
    """

    pass


class TransactionHasNotStartedError(BaseTransactionContextException):
    """
    Транзакция не начата - не вошли в контекстный менеджер
    """

    pass


class AsyncReadOnlyTransactionContext(AbstractAsyncContextManager[Any]):
    """
    Контекст БД только для чтения
    """

    def __init__(self, **kwargs: Any):
        self.create_session = async_sessionmaker(**kwargs)

        self._context_sessions: ContextVar[AsyncSession] = ContextVar("context_sessions")

        self._context_is_in_transaction: ContextVar[bool] = ContextVar("context_is_in_transaction")

    def _get_session_if_exists(self) -> AsyncSession | None:
        return self._context_sessions.get(None)

    @property
    def current_session(self) -> AsyncSession:
        if not self._context_is_in_transaction.get(False):
            raise TransactionHasNotStartedError(
                "The transaction has not started or has already been completed."
                "The action must be performed inside the context manager."
            )
        session = self._get_session_if_exists()
        if session is None:
            session = self.create_session()
            self._context_sessions.set(session)
            self._context_is_in_transaction.set(True)
        return session

    async def __aenter__(self) -> "AsyncReadOnlyTransactionContext":
        self._context_is_in_transaction.set(True)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
        /,
    ) -> bool | None:
        self._context_is_in_transaction.set(False)
        session = self._get_session_if_exists()
        if session is None:
            return None

        await session.rollback()
        await session.close()
        return False


class AsyncTransactionContext(AsyncReadOnlyTransactionContext):
    """
    Контекст БД
    """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
        /,
    ) -> bool | None:
        self._context_is_in_transaction.set(False)
        session = self._get_session_if_exists()
        if session is None:
            return None

        if exc_type is None:
            await session.commit()
        else:
            await session.rollback()

        await session.close()
        return False


class QueryBuilder:
    """Утилитарный класс для построения запросов"""

    @staticmethod
    def add_pagination(
        query: Select[Any],
        paginated_request: PaginatedRequestDto,
    ) -> Select[Any]:
        """Добавляет условия пагинации"""

        offset = (paginated_request.page - 1) * paginated_request.page_size

        query = query.limit(paginated_request.page_size)
        query = query.offset(offset)

        return query

    @staticmethod
    def create_total_items_query_for_table(
        query: Select[Any],
    ) -> Select[tuple[int]]:
        """Создаёт запрос на подсчёт количества записй по запросу"""
        count_query = select(func.count()).select_from(query.subquery())
        return count_query


class BaseReadOnlyRepository:
    """
    Базовый класс репозитория только для чтения
    """

    def __init__(self, transaction_context: AsyncReadOnlyTransactionContext):
        self._transaction_context = transaction_context
        self.query_builder = QueryBuilder()

    @property
    def session(self) -> AsyncSession:
        return self._transaction_context.current_session

    async def get_total_items(
        self,
        query: Select[Any],
    ) -> int:
        """Получает количество записей в таблице по условиям"""

        count_query = self.query_builder.create_total_items_query_for_table(query=query)
        total = (await self.session.execute(count_query)).scalar_one()
        return total

    def get_pages_count(self, total: int, page_size: int) -> int:
        return ceil(total / page_size) if total else 1


class BaseRepository(BaseReadOnlyRepository):
    """
    Базовый класс репозитория
    """

    def __init__(self, transaction_context: AsyncTransactionContext):
        super().__init__(transaction_context)
