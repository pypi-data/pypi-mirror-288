from uuid import uuid4
import typing

import sqlalchemy as sqla

from . import _directives_


class query:
    """
    Represents an sql query template that generates an sql statement (via jinja2).
    """

    def __init__(
        self,
        source: str,
    ) -> None:
        self.source: str = source
        self.parameters: typing.MutableMapping

    def bind_parameter(
        self,
        value: typing.Any,
    ) -> str:
        u4 = uuid4()
        k = f'p{u4.hex}'
        self.parameters[k] = value
        return k

    def render(
        self,
        parameters: typing.MutableMapping,
    ) -> str:
        self.parameters = parameters or {}
        _directives_.jinja2environment.globals['query'] = self
        try:
            template = _directives_.jinja2environment.from_string(self.source)
            return template.render(**parameters)
        finally:
            _directives_.jinja2environment.globals.pop('query')

    def compile(
        self,
        parameters: typing.MutableMapping,
    ) -> sqla.TextClause:
        raw_statement = self.render(parameters)
        return sqla.text(raw_statement)
