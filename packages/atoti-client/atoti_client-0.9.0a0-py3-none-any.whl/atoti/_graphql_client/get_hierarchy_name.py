from typing import Optional

from .base_model import BaseModel


class GetHierarchyName(BaseModel):
    cube: Optional["GetHierarchyNameCube"]


class GetHierarchyNameCube(BaseModel):
    dimension: Optional["GetHierarchyNameCubeDimension"]


class GetHierarchyNameCubeDimension(BaseModel):
    name: str
    hierarchy: Optional["GetHierarchyNameCubeDimensionHierarchy"]


class GetHierarchyNameCubeDimensionHierarchy(BaseModel):
    name: str


GetHierarchyName.model_rebuild()
GetHierarchyNameCube.model_rebuild()
GetHierarchyNameCubeDimension.model_rebuild()
