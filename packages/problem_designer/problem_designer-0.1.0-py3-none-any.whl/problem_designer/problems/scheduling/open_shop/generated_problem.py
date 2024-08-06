from pydantic import BaseModel


class ParameterError(RuntimeError):
    pass


class Task(BaseModel):
    task_id: str
    job_id: str
    resource_ids: list[str]
    processing_time: int


class Timespan(BaseModel):
    start: int
    end: int


class Resource(BaseModel):
    resource_id: str
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
