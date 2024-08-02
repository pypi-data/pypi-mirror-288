from typing import Optional

from .base_model import BaseModel


class GetTableName(BaseModel):
    table: Optional["GetTableNameTable"]


class GetTableNameTable(BaseModel):
    name: str


GetTableName.model_rebuild()
