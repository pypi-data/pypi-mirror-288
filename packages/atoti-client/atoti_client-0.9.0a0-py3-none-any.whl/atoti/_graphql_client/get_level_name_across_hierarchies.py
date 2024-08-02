from typing import List, Optional

from .base_model import BaseModel


class GetLevelNameAcrossHierarchies(BaseModel):
    cube: Optional["GetLevelNameAcrossHierarchiesCube"]


class GetLevelNameAcrossHierarchiesCube(BaseModel):
    dimensions: List["GetLevelNameAcrossHierarchiesCubeDimensions"]


class GetLevelNameAcrossHierarchiesCubeDimensions(BaseModel):
    name: str
    hierarchies: List["GetLevelNameAcrossHierarchiesCubeDimensionsHierarchies"]


class GetLevelNameAcrossHierarchiesCubeDimensionsHierarchies(BaseModel):
    level: Optional["GetLevelNameAcrossHierarchiesCubeDimensionsHierarchiesLevel"]
    name: str


class GetLevelNameAcrossHierarchiesCubeDimensionsHierarchiesLevel(BaseModel):
    name: str


GetLevelNameAcrossHierarchies.model_rebuild()
GetLevelNameAcrossHierarchiesCube.model_rebuild()
GetLevelNameAcrossHierarchiesCubeDimensions.model_rebuild()
GetLevelNameAcrossHierarchiesCubeDimensionsHierarchies.model_rebuild()
