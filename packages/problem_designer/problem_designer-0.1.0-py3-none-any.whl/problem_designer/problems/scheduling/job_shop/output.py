import logging
import os.path
import uuid
from pathlib import Path
from typing import Literal, Protocol

from problem_designer.problems.scheduling.generator.typedef import (
    IntermediateGeneratedProblem,
)
from problem_designer.problems.scheduling.job_shop.generated_problem import (
    GeneratedProblem,
    Job,
    Resource,
    Task,
)

logger = logging.getLogger(__name__)


def _encode_file_path(igp: IntermediateGeneratedProblem, file_ending: str) -> str:
    """
    Encodes the problem into a file name
    Args:
        igp: The generated problem
        file_ending: Which ending should be used

    Returns: the file name
    """
    return "_".join(
        [igp.problem_configuration.meta.get_global_identifier(), str(igp.number_of_jobs), str(igp.number_of_machines)]
    )


def write_json(igp: IntermediateGeneratedProblem, path: Path) -> Path:
    tasks = {}
    jobs = {}
    resources = {}

    for job_id, processing_times in igp.job_to_processing_times.items():
        # create job
        jobs[job_id] = Job(
            job_id=job_id,
            tasks=[],
            due_date=None,
            release_time=None,
        )
        # create tasks of job -> amount of tasks equal to amount of machines
        for i in range(igp.number_of_machines):
            task_id = str(uuid.uuid4())
            tasks[task_id] = Task(
                task_id=task_id,
                job_id=job_id,
                processing_time=processing_times[i],
                resource_ids=[str(i)],
                capacity_demand=1,
            )
            jobs[job_id].tasks.append(str(task_id))
            # create machines
            machine_id = str(i)
            if machine_id not in resources:
                resources[machine_id] = Resource(
                    resource_id=machine_id,
                    transportation_times=igp.machine_to_transportation_times[i],
                    capacities=igp.machine_capacity[machine_id],
                    default_capacity=igp.default_capacities[machine_id],
                    setup_times=None,
                    teardown_times=None,
                    unavailable_times=None,
                )

    gp = GeneratedProblem(
        tasks=tasks,
        resources=resources,
        jobs=jobs,
    )

    if os.path.isdir(str(path)):
        # if path is a directory, append filename and ending
        path = Path(str(path) + "\\output.json")
    # save json file and schema
    with open(path, "w") as f:
        f.write(gp.json(indent=2))
    with open(f"{str(path)}.schema", "w") as f:
        f.write(gp.schema_json(indent=2))
    logger.info("Successfully saved " + str(path))
    return path


def write_standard(igp: IntermediateGeneratedProblem, path: Path) -> Path:
    raise NotImplementedError


def write_taillard(igp: IntermediateGeneratedProblem, path: Path) -> Path:
    raise NotImplementedError


class Writer(Protocol):
    def write(self, igp: IntermediateGeneratedProblem):
        raise NotImplementedError


class JobShopWriter:
    def __init__(
        self,
        output_path: Path,
        format: Literal["taillard", "standard", "json"],
        **kwargs,
    ):
        super().__init__()
        self._output_path = output_path
        self._format = format

    def write(self, igp: IntermediateGeneratedProblem):
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        if self._format == "taillard":
            logger.info(write_taillard(igp, self._output_path))
        elif self._format == "json":
            logger.info(write_json(igp, self._output_path))
        else:
            logger.info(write_standard(igp, self._output_path))
