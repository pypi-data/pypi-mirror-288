from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class GetDimensionDefaultHierarchyName(BaseModel):
    cube: Optional["GetDimensionDefaultHierarchyNameCube"]


class GetDimensionDefaultHierarchyNameCube(BaseModel):
    dimension: Optional["GetDimensionDefaultHierarchyNameCubeDimension"]


class GetDimensionDefaultHierarchyNameCubeDimension(BaseModel):
    default_hierarchy: (
        "GetDimensionDefaultHierarchyNameCubeDimensionDefaultHierarchy"
    ) = Field(alias="defaultHierarchy")


class GetDimensionDefaultHierarchyNameCubeDimensionDefaultHierarchy(BaseModel):
    name: str


GetDimensionDefaultHierarchyName.model_rebuild()
GetDimensionDefaultHierarchyNameCube.model_rebuild()
GetDimensionDefaultHierarchyNameCubeDimension.model_rebuild()
