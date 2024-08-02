from typing import List, Optional

from .base_model import BaseModel


class GetHierarchyNameAcrossDimensions(BaseModel):
    cube: Optional["GetHierarchyNameAcrossDimensionsCube"]


class GetHierarchyNameAcrossDimensionsCube(BaseModel):
    dimensions: List["GetHierarchyNameAcrossDimensionsCubeDimensions"]


class GetHierarchyNameAcrossDimensionsCubeDimensions(BaseModel):
    name: str
    hierarchy: Optional["GetHierarchyNameAcrossDimensionsCubeDimensionsHierarchy"]


class GetHierarchyNameAcrossDimensionsCubeDimensionsHierarchy(BaseModel):
    name: str


GetHierarchyNameAcrossDimensions.model_rebuild()
GetHierarchyNameAcrossDimensionsCube.model_rebuild()
GetHierarchyNameAcrossDimensionsCubeDimensions.model_rebuild()
