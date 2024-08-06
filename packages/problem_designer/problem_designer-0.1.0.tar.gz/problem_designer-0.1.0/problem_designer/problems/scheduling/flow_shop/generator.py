from pathlib import Path
from typing import Literal

from pydantic import Field

from problem_designer.problems.scheduling.flow_shop.output import FlowShopWriter
from problem_designer.problems.scheduling.flow_shop.spec import (
    FlowShopDesignSpec,
    FlowShopParameters,
)
from problem_designer.problems.scheduling.generator.helper import (
    GenerateAmountOfStages,
    GenerateDemands,
    GenerateFixedIndexMappingFromStageToMachine,
    GenerateFixedIndexMappingToMachine,
    GenerateFixedNumberOfTasksPerJob,
    GenerateProcessingTimes,
    GenerateTransportationTimesForMachinesWithStages,
)
from problem_designer.problems.scheduling.generator.typedef import (
    IntermediateGeneratedProblem,
)
from problem_designer.typedef.generator import Generator, GeneratorOptions


class FlowShopGeneratorOptions(GeneratorOptions):
    output_path: Path = Field(
        description="Path to output path (will be created if it does not exist)",
        cli=("-o", "--output-path"),
    )
    format: Literal["taillard", "standard", "json"] = Field(default="json", description="Output format")


class FlowShopGenerator(Generator):
    def __init__(
        self,
        spec: FlowShopDesignSpec,
        options: FlowShopGeneratorOptions,
    ):
        self.spec = spec
        self.parameters_space = spec.parameter_space
        self.options = options
        # self.writer = ShopWriter
        self.writer = FlowShopWriter

    def execute(self, parameters: FlowShopParameters) -> IntermediateGeneratedProblem:
        pipeline = [
            GenerateFixedNumberOfTasksPerJob(
                number_of_jobs=parameters.number_of_jobs, number_of_tasks_per_job=parameters.number_of_stages
            ),
            GenerateAmountOfStages(number_of_stages=parameters.number_of_stages),
            GenerateFixedIndexMappingToMachine(number_of_machines=parameters.number_of_machines),
            GenerateProcessingTimes(self.spec.characteristics.processing_time),
            GenerateFixedIndexMappingFromStageToMachine(),
            GenerateTransportationTimesForMachinesWithStages(self.spec.characteristics.transportation_time),
            GenerateDemands(dc=self.spec.characteristics.demands),
        ]
        igp = IntermediateGeneratedProblem(problem_configuration=self.spec)
        for step in pipeline:
            igp = step.generate(igp)
        return igp

    def generate(self):
        for parameters in self.parameters_space.get_parameter_grid():
            # calculate
            igp = self.execute(parameters)
            # write output files
            self.writer(**self.options.dict()).write(igp)
