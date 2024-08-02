from typing import List, Optional

from .base_model import BaseModel


class GetLevelNames(BaseModel):
    cube: Optional["GetLevelNamesCube"]


class GetLevelNamesCube(BaseModel):
    dimensions: List["GetLevelNamesCubeDimensions"]


class GetLevelNamesCubeDimensions(BaseModel):
    name: str
    hierarchies: List["GetLevelNamesCubeDimensionsHierarchies"]


class GetLevelNamesCubeDimensionsHierarchies(BaseModel):
    levels: List["GetLevelNamesCubeDimensionsHierarchiesLevels"]
    name: str
    slicing: bool


class GetLevelNamesCubeDimensionsHierarchiesLevels(BaseModel):
    name: str


GetLevelNames.model_rebuild()
GetLevelNamesCube.model_rebuild()
GetLevelNamesCubeDimensions.model_rebuild()
GetLevelNamesCubeDimensionsHierarchies.model_rebuild()
