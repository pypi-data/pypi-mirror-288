from typing import List

from .base_model import BaseModel


class GetTableNames(BaseModel):
    tables: List["GetTableNamesTables"]


class GetTableNamesTables(BaseModel):
    name: str


GetTableNames.model_rebuild()
