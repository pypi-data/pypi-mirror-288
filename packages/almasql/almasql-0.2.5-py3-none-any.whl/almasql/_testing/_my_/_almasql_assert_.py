import typing
import almasql
from . import _settings_


async def almasql_assert(
    _function: typing.Callable[[typing.Any], bool],
    _query: almasql.query | str,
    _exception: typing.Any = None,
    **kwargs,
):
    async with almasql.new_transaction(_settings_.engine) as transaction:
        query_result = await transaction.execute(_query, **kwargs)
        condition = _function(*query_result)
        message = f'query result: {query_result}'
        assert condition, message if _exception is None else (_exception, message)
