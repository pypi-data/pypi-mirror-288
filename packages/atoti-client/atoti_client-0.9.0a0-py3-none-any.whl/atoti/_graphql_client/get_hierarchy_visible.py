from typing import Optional

from .base_model import BaseModel


class GetHierarchyVisible(BaseModel):
    cube: Optional["GetHierarchyVisibleCube"]


class GetHierarchyVisibleCube(BaseModel):
    dimension: Optional["GetHierarchyVisibleCubeDimension"]


class GetHierarchyVisibleCubeDimension(BaseModel):
    name: str
    hierarchy: Optional["GetHierarchyVisibleCubeDimensionHierarchy"]


class GetHierarchyVisibleCubeDimensionHierarchy(BaseModel):
    visible: bool


GetHierarchyVisible.model_rebuild()
GetHierarchyVisibleCube.model_rebuild()
GetHierarchyVisibleCubeDimension.model_rebuild()
