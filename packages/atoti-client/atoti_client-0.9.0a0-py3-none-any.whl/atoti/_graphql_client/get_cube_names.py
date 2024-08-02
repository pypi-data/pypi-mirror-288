from typing import List

from .base_model import BaseModel


class GetCubeNames(BaseModel):
    cubes: List["GetCubeNamesCubes"]


class GetCubeNamesCubes(BaseModel):
    name: str


GetCubeNames.model_rebuild()
