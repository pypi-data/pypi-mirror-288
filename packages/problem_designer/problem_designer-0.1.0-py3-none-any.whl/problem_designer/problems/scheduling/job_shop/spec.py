from problem_designer.problems.scheduling.constants.characteristic import (
    PrecedenceRelation,
    ProcessingTimeCharacteristic,
    TransportationTimeCharacteristic,
)
from problem_designer.problems.scheduling.constants.objective import SupportedObjectives
from problem_designer.typedef.helper import Range
from problem_designer.typedef.parameter_grid import SpecParameterGrid
from problem_designer.typedef.spec import MetaInfo, StrictBaseModel, StrictDesignSpec


class JobShopMeta(MetaInfo):
    category: str = "scheduling"
    id: str = "job-shop"


class JobShopParameters(SpecParameterGrid):
    number_of_jobs: int | list[int] | Range
    number_of_machines: int | list[int] | Range
    capacity_of_machines: dict[str, dict[str, int]]
    default_capacities: int | dict[str, int] | Range


class JobShopCharacteristics(StrictBaseModel):
    processing_time: ProcessingTimeCharacteristic
    transportation_time: TransportationTimeCharacteristic
    precedence: PrecedenceRelation = PrecedenceRelation()


class JobShopDesignSpec(StrictDesignSpec):
    """
    The Job Shop problem is a scheduling problem where multiple jobs are processed on several machines.
    """

    meta: MetaInfo = JobShopMeta()
    parameter_space: JobShopParameters
    characteristics: JobShopCharacteristics
    objectives: list[SupportedObjectives]
