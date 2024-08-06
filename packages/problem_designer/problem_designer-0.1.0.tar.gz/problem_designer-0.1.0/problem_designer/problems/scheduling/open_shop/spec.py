from problem_designer.problems.scheduling.constants.characteristic import (
    NoPrecedenceRelation,
    ProcessingTimeCharacteristic,
)
from problem_designer.problems.scheduling.constants.objective import SupportedObjectives
from problem_designer.typedef.helper import Range
from problem_designer.typedef.parameter_grid import SpecParameterGrid
from problem_designer.typedef.spec import MetaInfo, StrictBaseModel, StrictDesignSpec


class OpenShopMeta(MetaInfo):
    category: str = "scheduling"
    id: str = "open-shop"


class OpenShopCharacteristics(StrictBaseModel):
    processing_time: ProcessingTimeCharacteristic
    precedence: NoPrecedenceRelation = NoPrecedenceRelation()


class OpenShopParameters(SpecParameterGrid):
    number_of_machines: int | list[int] | Range
    number_of_jobs: int | list[int] | Range


class OpenShopDesignSpec(StrictDesignSpec):
    """
    The Open Shop problem is a job shop problem which does not define a precedence.
    """

    meta: MetaInfo = OpenShopMeta()
    parameter_space: OpenShopParameters
    characteristics: OpenShopCharacteristics
    objectives: list[SupportedObjectives]
