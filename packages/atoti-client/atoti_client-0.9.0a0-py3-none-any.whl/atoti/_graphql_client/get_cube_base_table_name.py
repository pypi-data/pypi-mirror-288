from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class GetCubeBaseTableName(BaseModel):
    cube: Optional["GetCubeBaseTableNameCube"]


class GetCubeBaseTableNameCube(BaseModel):
    base_table: "GetCubeBaseTableNameCubeBaseTable" = Field(alias="baseTable")


class GetCubeBaseTableNameCubeBaseTable(BaseModel):
    name: str


GetCubeBaseTableName.model_rebuild()
GetCubeBaseTableNameCube.model_rebuild()
