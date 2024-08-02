from typing import Optional

from .base_model import BaseModel


class GetCubeName(BaseModel):
    cube: Optional["GetCubeNameCube"]


class GetCubeNameCube(BaseModel):
    name: str


GetCubeName.model_rebuild()
