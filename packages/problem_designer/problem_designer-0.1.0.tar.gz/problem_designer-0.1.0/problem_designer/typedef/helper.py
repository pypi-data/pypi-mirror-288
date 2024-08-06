from typing import Literal, Protocol, runtime_checkable

import numpy as np
from pydantic import BaseModel

from problem_designer.typedef.spec import StrictBaseModel


class UniformDistribution(StrictBaseModel):
    type: Literal["uniform"]
    lower_bound: int = 0
    upper_bound: int = 100
    seed: int | None = None

    def take_n(self, n: int) -> list[int]:
        return list(
            np.random.default_rng(seed=self.seed).integers(self.lower_bound, self.upper_bound, n, endpoint=True)
        )

    def take_one(self) -> int:
        return np.random.default_rng().integers(self.lower_bound, self.upper_bound, endpoint=True)


class Constant(BaseModel):
    type: Literal["constant"] = "constant"
    value: int = 1

    def take_n(self, n: int) -> list[int]:
        return [self.value] * n


class RandomValue(BaseModel):
    lower_bound: int = 0
    upper_bound: int = 10

    def get_random_value(self) -> int:
        return np.random.randint(low=self.lower_bound, high=self.upper_bound)


@runtime_checkable
class SupportsParameterGrid(Protocol):
    """
    A protocol which can be checked at runtime with isinstance. Allow to check if a parameter needs
    special attention during creation of a parameter grid
    """

    def evaluate_for_parameter_grid(self):
        raise NotImplementedError


class Range(BaseModel):
    type: Literal["range"] = "range"
    lower_bound: int = 0
    upper_bound: int = 100
    step: int = 1

    def evaluate_for_parameter_grid(self):
        return list(range(self.lower_bound, self.upper_bound + 1, self.step))


SupportedDistribution = UniformDistribution | Constant
