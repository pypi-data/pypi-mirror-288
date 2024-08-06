from pydantic import BaseModel


class ParameterError(RuntimeError):
    pass


class Task(BaseModel):
    task_id: str
    job_id: str
    resource_ids: list[str]
    # stage: int | None
    processing_time: int
    capacity_demand: int


class Timespan(BaseModel):
    start: int
    end: int


class Resource(BaseModel):
    resource_id: str
    transportation_times: dict[str, int] | None  # key = to_machine, value = transportation_time
    capacities: dict[str, int] | None  # key = interval, value = capacity
    default_capacity: int | None
    setup_times: dict[str, int] | None
    teardown_times: dict[str, Timespan] | None
    unavailable_times: dict[str, Timespan] | None


class Job(BaseModel):
    job_id: str
    tasks: list[str | list[str]]
    due_date: str | None
    release_time: str | None


class GeneratedProblem(BaseModel):
    tasks: dict[str, Task]
    jobs: dict[str, Job]
    resources: dict[str, Resource]
