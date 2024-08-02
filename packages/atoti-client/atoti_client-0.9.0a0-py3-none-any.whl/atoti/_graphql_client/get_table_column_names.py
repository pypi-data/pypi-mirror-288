from typing import List, Optional

from .base_model import BaseModel


class GetTableColumnNames(BaseModel):
    table: Optional["GetTableColumnNamesTable"]


class GetTableColumnNamesTable(BaseModel):
    columns: List["GetTableColumnNamesTableColumns"]


class GetTableColumnNamesTableColumns(BaseModel):
    name: str


GetTableColumnNames.model_rebuild()
GetTableColumnNamesTable.model_rebuild()
