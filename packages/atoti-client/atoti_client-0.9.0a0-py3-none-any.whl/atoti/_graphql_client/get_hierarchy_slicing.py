from typing import Optional

from .base_model import BaseModel


class GetHierarchySlicing(BaseModel):
    cube: Optional["GetHierarchySlicingCube"]


class GetHierarchySlicingCube(BaseModel):
    dimension: Optional["GetHierarchySlicingCubeDimension"]


class GetHierarchySlicingCubeDimension(BaseModel):
    name: str
    hierarchy: Optional["GetHierarchySlicingCubeDimensionHierarchy"]


class GetHierarchySlicingCubeDimensionHierarchy(BaseModel):
    slicing: bool


GetHierarchySlicing.model_rebuild()
GetHierarchySlicingCube.model_rebuild()
GetHierarchySlicingCubeDimension.model_rebuild()
