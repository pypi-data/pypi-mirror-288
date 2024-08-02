from typing import List, Optional

from .base_model import BaseModel


class GetHierarchyNames(BaseModel):
    cube: Optional["GetHierarchyNamesCube"]


class GetHierarchyNamesCube(BaseModel):
    dimensions: List["GetHierarchyNamesCubeDimensions"]


class GetHierarchyNamesCubeDimensions(BaseModel):
    name: str
    hierarchies: List["GetHierarchyNamesCubeDimensionsHierarchies"]


class GetHierarchyNamesCubeDimensionsHierarchies(BaseModel):
    name: str


GetHierarchyNames.model_rebuild()
GetHierarchyNamesCube.model_rebuild()
GetHierarchyNamesCubeDimensions.model_rebuild()
