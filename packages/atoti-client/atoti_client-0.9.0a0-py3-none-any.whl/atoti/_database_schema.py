from __future__ import annotations

import re
from collections.abc import Mapping, Set as AbstractSet
from dataclasses import field
from typing import Annotated, Literal, final

from pydantic import Field
from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._collections import FrozenMapping, FrozenSequence
from ._column_description import ColumnDescription
from ._mermaid_diagram import MermaidDiagram
from ._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG

RelationshipOptionality = Literal["mandatory", "optional"]

_QUOTE = '"'


def _validate_attribute_word(value: str, /) -> str:
    if (
        re.match(
            # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L28C8-L28C42.
            r"[\*A-Za-z_][A-Za-z0-9\-_\[\]\(\)]*",
            value,
        )
        is None
    ):
        raise ValueError(f"Invalid attribute word: `{value}`.")

    return value


def _validate_word(value: str, /) -> str:
    if _QUOTE in value:
        # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L21.
        raise ValueError(f"""Unsupported `{_QUOTE}` in `{value}`""")

    return value


def _quote(value: str, /) -> str:
    # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L29.
    return f"{_QUOTE}{_validate_word(value)}{_QUOTE}"


def _column_to_attribute(column: ColumnDescription, /, *, is_key: bool) -> str:
    # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L26.
    key_attribute = "PK"
    # See https://github.com/mermaid-js/mermaid/blob/6e6455632668f5f674ea43bd49ac1a653d232f0c/packages/mermaid/src/diagrams/er/parser/erDiagram.jison#L127-L132.
    # Mermaid supports a very restricted set of characters in attribute names.
    # See https://github.com/mermaid-js/mermaid/issues/1895.
    # To work around this, the column name is declared in the attribute comment, the column nullability is declared in the attribute type and the column data type is declared in the attribute name.
    return " ".join(
        [
            _validate_attribute_word("nullable" if column.nullable else "_"),
            _validate_attribute_word(column.data_type),
            *([key_attribute] if is_key else []),
            _quote(column.name),
        ],
    )


_TARGET_OPTIONALITY_AND_PARTIAL_JOINTNESS_TO_CARDINALITY: Mapping[
    RelationshipOptionality,
    Mapping[bool, str],
] = {"mandatory": {True: "|{", False: "||"}, "optional": {True: "o{", False: "o|"}}


def _get_relationship(join: JoinDescription, /) -> str:
    source_cardinality = "}o"
    target_cardinality = _TARGET_OPTIONALITY_AND_PARTIAL_JOINTNESS_TO_CARDINALITY[
        join.target_optionality
    ][join.partial]
    return (
        f"""{source_cardinality}{".." if join.partial else "--"}{target_cardinality}"""
    )


def _get_relationship_label(join: JoinDescription, /) -> str:
    def parenthesize(value: str, /) -> str:
        return value if len(join.mapping) == 1 else f"({value})"

    return " & ".join(
        parenthesize(
            f"`{_validate_word(source_column_name)}` == `{_validate_word(target_column_name)}`",
        )
        for source_column_name, target_column_name in join.mapping.items()
    )


def _generate_mermaid_diagram_code(schema: DatabaseSchema, /) -> str:
    indent = "  "
    lines: list[str] = ["erDiagram"]

    for table in sorted(schema.tables):
        lines.append(f"{indent}{_quote(table.name)} {{")

        lines.extend(
            f"{indent}{indent}{_column_to_attribute(column, is_key=column.name in sorted(table.keys))}"
            for column in table.columns
        )

        lines.append(f"{indent}}}")

    lines.extend(
        " ".join(
            [
                f"{indent}{_quote(join.source_table_name)}",
                _get_relationship(join),
                _quote(join.target_table_name),
                f": {_quote(_get_relationship_label(join))}",
            ],
        )
        for join in sorted(schema.joins)
    )

    lines.append("")

    return "\n".join(lines)


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True, order=True)
class JoinDescription:
    source_table_name: str
    target_table_name: str
    partial: bool
    mapping: FrozenMapping[str, str] = field(compare=False)
    target_optionality: RelationshipOptionality = "optional"


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True, order=True)
class TableDescription:
    name: str
    columns: Annotated[FrozenSequence[ColumnDescription], Field(min_length=1)]
    keys: AbstractSet[str]


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True, kw_only=True, order=True)
class DatabaseSchema(MermaidDiagram):
    joins: AbstractSet[JoinDescription]
    tables: AbstractSet[TableDescription]

    @property
    @override
    def _mermaid_diagram_code(self) -> str:
        return _generate_mermaid_diagram_code(self)

    @override
    def __repr__(self) -> str:
        return super().__repr__()
