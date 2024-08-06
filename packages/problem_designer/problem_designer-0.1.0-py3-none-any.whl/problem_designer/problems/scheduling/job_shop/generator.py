from pathlib import Path
from typing import Literal

from pydantic import Field

from problem_designer.problems.scheduling.generator.helper import (
    GenerateFixedIndexMappingToMachine,
    GenerateFixedNumberOfTasksPerJob,
    GenerateMachineCapacities,
    GenerateProcessingTimes,
    GenerateTransportationTimes,
)
from problem_designer.problems.scheduling.generator.typedef import (
    IntermediateGeneratedProblem,
)
from problem_designer.problems.scheduling.job_shop.output import JobShopWriter
from problem_designer.problems.scheduling.job_shop.spec import (
    JobShopDesignSpec,
    JobShopParameters,
)
from problem_designer.typedef.generator import Generator, GeneratorOptions


class JobShopGeneratorOptions(GeneratorOptions):
    output_path: Path = Field(
        description="Path to output path (will be created if it does not exist)",
        cli=("-o", "--output-path"),
    )
    format: Literal["taillard", "standard", "json"] = Field(default="json", description="Output format")


class JobShopGenerator(Generator):
    def __init__(self, spec: JobShopDesignSpec, options: JobShopGeneratorOptions):
        self.spec = spec
        self.parameters_space = spec.parameter_space
        self.options = options
        self.writer = JobShopWriter

    def execute(self, parameters: JobShopParameters) -> IntermediateGeneratedProblem:
        pipeline = [
            GenerateFixedNumberOfTasksPerJob(
                number_of_jobs=parameters.number_of_jobs,
                number_of_tasks_per_job=parameters.number_of_machines,
            ),
            GenerateFixedIndexMappingToMachine(number_of_machines=parameters.number_of_machines),
            GenerateProcessingTimes(pt=self.spec.characteristics.processing_time),
            GenerateTransportationTimes(tt=self.spec.characteristics.transportation_time),
            GenerateMachineCapacities(cp=parameters.capacity_of_machines, default_cap=parameters.default_capacities),
        ]
        igp = IntermediateGeneratedProblem(problem_configuration=self.spec)
        for step in pipeline:
            igp = step.generate(igp)
        return igp

    def generate(self):
        for parameters in self.parameters_space.get_parameter_grid():
            igp = self.execute(parameters)
            self.writer(**self.options.dict()).write(igp)
