from typing import List, Optional

from .base_model import BaseModel


class GetHierarchyLevelNames(BaseModel):
    cube: Optional["GetHierarchyLevelNamesCube"]


class GetHierarchyLevelNamesCube(BaseModel):
    dimension: Optional["GetHierarchyLevelNamesCubeDimension"]


class GetHierarchyLevelNamesCubeDimension(BaseModel):
    name: str
    hierarchy: Optional["GetHierarchyLevelNamesCubeDimensionHierarchy"]


class GetHierarchyLevelNamesCubeDimensionHierarchy(BaseModel):
    levels: List["GetHierarchyLevelNamesCubeDimensionHierarchyLevels"]
    name: str
    slicing: bool


class GetHierarchyLevelNamesCubeDimensionHierarchyLevels(BaseModel):
    name: str


GetHierarchyLevelNames.model_rebuild()
GetHierarchyLevelNamesCube.model_rebuild()
GetHierarchyLevelNamesCubeDimension.model_rebuild()
GetHierarchyLevelNamesCubeDimensionHierarchy.model_rebuild()
