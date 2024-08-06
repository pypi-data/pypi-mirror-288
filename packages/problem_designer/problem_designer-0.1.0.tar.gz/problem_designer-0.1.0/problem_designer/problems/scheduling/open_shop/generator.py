from pathlib import Path
from typing import Literal

from pydantic import Field

from problem_designer.problems.scheduling.generator.helper import (
    GenerateFixedIndexMappingToMachine,
    GenerateFixedNumberOfTasksPerJob,
    GenerateProcessingTimes,
)
from problem_designer.problems.scheduling.generator.typedef import (
    IntermediateGeneratedProblem,
)
from problem_designer.problems.scheduling.open_shop.output import OpenShopWriter
from problem_designer.problems.scheduling.open_shop.spec import OpenShopDesignSpec
from problem_designer.typedef.generator import Generator, GeneratorOptions


class OpenShopGeneratorOptions(GeneratorOptions):
    output_path: Path = Field(
        description="Path to output path (will be created if it does not exist)",
        cli=("-o", "--output-path"),
    )
    format: Literal["taillard", "standard", "json"] = Field(default="json", description="Output format")


class OpenShopGenerator(Generator):
    def __init__(
        self,
        spec: OpenShopDesignSpec,
        options: OpenShopGeneratorOptions,
    ):
        self.spec = spec
        self.parameters_space = spec.parameter_space
        self.options = options
        self.writer = OpenShopWriter

    def execute(self, parameters) -> IntermediateGeneratedProblem:
        pipeline = [
            GenerateFixedNumberOfTasksPerJob(
                parameters.number_of_jobs,
                parameters.number_of_machines,
            ),
            GenerateFixedIndexMappingToMachine(parameters.number_of_machines),
            GenerateProcessingTimes(self.spec.characteristics.processing_time),
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
