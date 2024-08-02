import almasql
import _my_


async def test_sqlite_basic():
    # Boolean
    await _my_.almasql_assert(
        lambda r: r == True,
        "select true",
    )
    await _my_.almasql_assert(
        lambda r: r == True,
        "select {{ true }}",
    )
    await _my_.almasql_assert(
        lambda r: r == True,
        "select :p",
        p=True,
    )
    # Integer
    await _my_.almasql_assert(
        lambda r: r == 7,
        "select 7",
    )
    await _my_.almasql_assert(
        lambda r: r == 7,
        "select {{ 7 }}",
    )
    await _my_.almasql_assert(
        lambda r: r == 7,
        "select :p",
        p=7,
    )
    # Float
    await _my_.almasql_assert(
        lambda r: r == 3.14,
        "select 3.14",
    )
    await _my_.almasql_assert(
        lambda r: r == 3.14,
        "select {{ 3.14 }}",
    )
    await _my_.almasql_assert(
        lambda r: r == 3.14,
        "select :p",
        p=3.14,
    )
    # String
    await _my_.almasql_assert(
        lambda r: r == 'almasql',
        "select 'almasql'",
    )
    await _my_.almasql_assert(
        lambda r: r == 'almasql',
        "select '{{ 'almasql' }}'",
    )
    await _my_.almasql_assert(
        lambda r: r == 'almasql',
        "select :p",
        p='almasql'
    )

    async with almasql.new_transaction(_my_.settings.engine) as transaction:
        await transaction.execute("drop table if exists book")

        await transaction.execute("""
            create table book(
                id integer primary key,
                title string,
                price float,
                is_active bool
            )
        """)

        values = {
            'title': 'why i love almasql?',
            'price': 3.14,
            'is_active': True,
        }
        (id, ) = await transaction.execute(
            "insert into book {{ values(x) }} returning id",
            x=values,
        )

        row = await transaction.fetch_one(
            "select * from book where id = {{ _(id) }}",
            id=id,
        )
        assert row

        rows = await transaction.fetch_one(
            "select * from book where id in ({{ unpack(ids) }})",
            ids=[id],
        )
        assert len(rows) > 0
