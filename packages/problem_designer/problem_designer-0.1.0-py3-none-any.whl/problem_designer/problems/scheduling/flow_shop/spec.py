from problem_designer.problems.scheduling.constants.characteristic import (
    DemandsCharacteristics,
    PrecedenceRelation,
    ProcessingTimeCharacteristic,
    TransportationTimeCharacteristic,
)
from problem_designer.problems.scheduling.constants.objective import SupportedObjectives
from problem_designer.typedef.helper import Range
from problem_designer.typedef.parameter_grid import SpecParameterGrid
from problem_designer.typedef.spec import MetaInfo, StrictBaseModel, StrictDesignSpec


class FlowShopMeta(MetaInfo):
    category: str = "scheduling"
    id: str = "flow-shop"


class FlowShopParameters(SpecParameterGrid):
    number_of_machines: int | list[int] | Range
    number_of_stages: int | list[int] | Range
    number_of_jobs: int | list[int] | Range


class FlowShopCharacteristics(StrictBaseModel):
    processing_time: ProcessingTimeCharacteristic
    transportation_time: TransportationTimeCharacteristic
    precedence: PrecedenceRelation = PrecedenceRelation()
    demands: DemandsCharacteristics


class FlowShopDesignSpec(StrictDesignSpec):
    """
    The Flow Shop problem is a job shop problem which has a strict order of operations to be performed on all jobs.
    """

    meta: MetaInfo = FlowShopMeta()
    parameter_space: FlowShopParameters
    characteristics: FlowShopCharacteristics
    objectives: list[SupportedObjectives]
