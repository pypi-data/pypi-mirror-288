from dataclasses import KW_ONLY
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from ._identifier_pydantic_config import IDENTIFIER_PYDANTIC_CONFIG
from .identifier import Identifier
from .table_name import TableName


@final
@dataclass(config=IDENTIFIER_PYDANTIC_CONFIG, frozen=True)
class TableIdentifier(Identifier):
    table_name: TableName
    _: KW_ONLY

    @override
    def __repr__(self) -> str:
        return f"""t["{self.table_name}"]"""
