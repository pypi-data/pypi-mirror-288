from typing import Optional

from .base_model import BaseModel


class GetLevelName(BaseModel):
    cube: Optional["GetLevelNameCube"]


class GetLevelNameCube(BaseModel):
    dimension: Optional["GetLevelNameCubeDimension"]


class GetLevelNameCubeDimension(BaseModel):
    name: str
    hierarchy: Optional["GetLevelNameCubeDimensionHierarchy"]


class GetLevelNameCubeDimensionHierarchy(BaseModel):
    level: Optional["GetLevelNameCubeDimensionHierarchyLevel"]
    name: str


class GetLevelNameCubeDimensionHierarchyLevel(BaseModel):
    name: str


GetLevelName.model_rebuild()
GetLevelNameCube.model_rebuild()
GetLevelNameCubeDimension.model_rebuild()
GetLevelNameCubeDimensionHierarchy.model_rebuild()
