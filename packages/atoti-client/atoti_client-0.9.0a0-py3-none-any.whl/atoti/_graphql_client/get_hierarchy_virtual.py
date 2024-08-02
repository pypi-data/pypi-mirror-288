from typing import Optional

from .base_model import BaseModel


class GetHierarchyVirtual(BaseModel):
    cube: Optional["GetHierarchyVirtualCube"]


class GetHierarchyVirtualCube(BaseModel):
    dimension: Optional["GetHierarchyVirtualCubeDimension"]


class GetHierarchyVirtualCubeDimension(BaseModel):
    name: str
    hierarchy: Optional["GetHierarchyVirtualCubeDimensionHierarchy"]


class GetHierarchyVirtualCubeDimensionHierarchy(BaseModel):
    virtual: bool


GetHierarchyVirtual.model_rebuild()
GetHierarchyVirtualCube.model_rebuild()
GetHierarchyVirtualCubeDimension.model_rebuild()
