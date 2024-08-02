import typing


Unset = ...


async def post_join[LI: object, RI: object, K: typing.Any](
    _attribute_: str,
    _from_: typing.Iterable[RI]
    | typing.Callable[[set[K]], typing.Awaitable[typing.Iterable[RI]]],
    _where_: typing.Callable[[RI], K],
    _equal_: typing.Callable[[LI], K],
    left: list[LI],
    /,
    many=False,
    default=Unset,
) -> None:
    """
    Joins list of subrecords from function to list of record by `_attribute_`.
    Group subrecords if many is True.
    Excludes record from `left` if subrecord not found and `default` is unset.

    ```python
    class Author:
        id: UUID
        full_name: str

    class Book:
        id: UUID
        name: str
        author_id: UUID

    async def get_authors(
        ids: set[UUID],
    ) -> list[Author]:
        '''Returns list of authors'''

    books = [<list of books>]
    await post_join(
        'authors',
        get_authors,
        lambda author: author.id,
        lambda book: book.author_id,
        books,
    )
    for b in books:
        list_of_authors = ', '.join([author.full_name for author in b.authors])
        print(f'book {b.name} published by {list_of_authors}')
    ```
    """
    left_map = {_equal_(i): i for i in left}

    if callable(_from_):
        pks = set(left_map.keys())
        right = await _from_(pks)
    else:
        right = _from_

    right_map = {}
    for i in right:  # type: ignore
        pk = _where_(i)
        if many:
            subitems = right_map.get(pk)
            if subitems is None:
                subitems = []
                right_map[pk] = subitems
            subitems.append(i)
        else:
            right_map[pk] = i

    for pk, left_item in left_map.items():
        right_item = right_map.get(pk, default)
        if right_item is Unset:
            left.remove(left_item)
            continue
        setattr(left_item, _attribute_, right_item)
