from contextlib import asynccontextmanager
import typing

import sqlalchemy as sqla
from sqlalchemy.ext.asyncio import (
    AsyncConnection as sqla_connection,
    AsyncEngine as sqla_engine,
)

from . import _query_
from . import _transactions_chain_


class active_transaction:
    """
    Represents an active transaction.
    """

    def __init__(
        self,
        sqlac: sqla_connection,
    ):
        self._sqlac = sqlac

    async def _ask(
        self,
        q: _query_.query | str,
        **parameters,
    ) -> sqla.CursorResult:
        if not isinstance(q, _query_.query):
            q = _query_.query(q)
        statement = q.compile(parameters)
        return await self._sqlac.execute(statement, parameters)

    async def fetch_one(
        self,
        q: _query_.query | str,
        **parameters,
    ) -> sqla.RowMapping | None:
        """
        Returns the first row of the query result.
        """
        result = await self._ask(q, **parameters)
        mapping_result = result.mappings()
        row = mapping_result.first()
        return row

    async def fetch_many(
        self,
        q: _query_.query | str,
        **parameters,
    ) -> typing.Sequence[sqla.RowMapping]:
        """
        Returns the list of the query result.
        """
        result = await self._ask(q, **parameters)
        mapping_result = result.mappings()
        rows = mapping_result.all()
        return rows

    async def execute(
        self,
        q: _query_.query | str,
        **parameters,
    ) -> sqla.Row | None:
        """
        Executes the query and returns the result.
        """
        result = await self._ask(q, **parameters)
        if result.returns_rows:
            returning = result.one()
            return returning


@asynccontextmanager
async def _make_transaction(
    engine: sqla_engine,
) -> typing.AsyncGenerator[active_transaction, None]:
    """
    Begin a new transaction.
    """
    async with engine.connect() as sqlac:
        async with sqlac.begin():
            yield active_transaction(sqlac)


@asynccontextmanager
async def new_transaction(
    engine: sqla_engine,
    *,
    use_last: bool = True,
    pretransaction_factory = _make_transaction
) -> typing.AsyncGenerator[active_transaction, None]:
    pretransaction = pretransaction_factory(engine)
    async with _transactions_chain_.add(
        pretransaction=pretransaction,
        use_last=use_last,
    ) as transaction:
        yield transaction
