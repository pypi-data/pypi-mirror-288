from typing import List, Optional

from .base_model import BaseModel


class GetTableKeys(BaseModel):
    table: Optional["GetTableKeysTable"]


class GetTableKeysTable(BaseModel):
    columns: List["GetTableKeysTableColumns"]
    keys: List[str]


class GetTableKeysTableColumns(BaseModel):
    name: str


GetTableKeys.model_rebuild()
GetTableKeysTable.model_rebuild()
