from typing import List, Optional

from .base_model import BaseModel


class GetLevelNameAcrossDimensions(BaseModel):
    cube: Optional["GetLevelNameAcrossDimensionsCube"]


class GetLevelNameAcrossDimensionsCube(BaseModel):
    dimensions: List["GetLevelNameAcrossDimensionsCubeDimensions"]


class GetLevelNameAcrossDimensionsCubeDimensions(BaseModel):
    name: str
    hierarchy: Optional["GetLevelNameAcrossDimensionsCubeDimensionsHierarchy"]


class GetLevelNameAcrossDimensionsCubeDimensionsHierarchy(BaseModel):
    level: Optional["GetLevelNameAcrossDimensionsCubeDimensionsHierarchyLevel"]
    name: str


class GetLevelNameAcrossDimensionsCubeDimensionsHierarchyLevel(BaseModel):
    name: str


GetLevelNameAcrossDimensions.model_rebuild()
GetLevelNameAcrossDimensionsCube.model_rebuild()
GetLevelNameAcrossDimensionsCubeDimensions.model_rebuild()
GetLevelNameAcrossDimensionsCubeDimensionsHierarchy.model_rebuild()
