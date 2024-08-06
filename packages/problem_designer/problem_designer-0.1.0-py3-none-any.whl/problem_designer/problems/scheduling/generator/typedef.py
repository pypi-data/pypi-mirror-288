from typing import Protocol

from pydantic import BaseModel, Field

from problem_designer.problems.scheduling.flow_shop.spec import FlowShopDesignSpec
from problem_designer.problems.scheduling.job_shop.spec import JobShopDesignSpec
from problem_designer.problems.scheduling.open_shop.spec import OpenShopDesignSpec


class IntermediateGeneratedProblem(BaseModel):
    problem_configuration: OpenShopDesignSpec | FlowShopDesignSpec | JobShopDesignSpec
    number_of_jobs: int | None = None
    total_number_of_tasks: int | None = None
    number_of_machines: int | None = None
    default_capacities: int | dict[str, int] | None = None
    number_of_stages: int | None = None
    number_of_machines_per_stage: int | None = None
    map_job_to_task_count: dict[str, int] = Field(default_factory=dict)
    map_machine_to_task: dict[str, list[int]] = Field(default_factory=dict)
    map_stage_to_machine: dict[str, list[int]] = Field(default_factory=dict)
    job_to_processing_times: dict[str, list[int]] = Field(default_factory=dict)
    machine_to_transportation_times: list[dict[str, int]] = Field(default_factory=list)
    machine_capacity: dict[str, dict[str, int]] = Field(default_factory=dict)
    demands: dict[str, dict[str, int]] = Field(default_factory=dict)
    constraints: list[str] = Field(default_factory=list)
    objectives: list[str] = Field(default_factory=list)


class GeneratorStep(Protocol):
    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        raise NotImplementedError
