from typing import Literal

from pydantic import BaseModel


class DefaultRandomSeed(BaseModel):
    type: Literal["random-seed"]
    seed: int
