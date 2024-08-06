from typing import List, Literal

from pydantic import BaseModel

from problem_designer.typedef.helper import Constant, RandomValue, UniformDistribution


class NoPrecedenceRelation(BaseModel):
    type: Literal["precedence-none"] = "precedence-none"


class PrecedenceRelation(BaseModel):
    type: Literal["precedence-prec"] = "precedence-prec"


class ProcessingTime(BaseModel):
    type: Literal["processing-time"] = "processing-time"
    distribution: Constant | UniformDistribution


class ProcessingTimePerJob(BaseModel):
    type: Literal["processing-time-per-job"] = "processing-time-per-job"
    distribution: List[Constant | UniformDistribution]


class TransportationTime(BaseModel):
    type: Literal["transportation-time"] = "transportation-time"
    distribution: RandomValue | Constant | UniformDistribution


class Demands(BaseModel):
    type: Literal["demands"] = "demands"
    distribution: UniformDistribution


PrecedenceCharacteristic = PrecedenceRelation
ProcessingTimeCharacteristic = ProcessingTime | ProcessingTimePerJob
TransportationTimeCharacteristic = TransportationTime
DemandsCharacteristics = Demands
