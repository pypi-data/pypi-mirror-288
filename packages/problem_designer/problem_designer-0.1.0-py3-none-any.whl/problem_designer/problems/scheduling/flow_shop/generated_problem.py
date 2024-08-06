from pydantic import BaseModel


class ParameterError(RuntimeError):
    pass


class Task(BaseModel):
    """
    A Task represents a single operation of a job.

    Attributes
    ----------
    task_id : str
        Unique Id of task
    job_id : str
        Unique Id of the job the tasks belongs to.
    resource_ids : list[str]
        List of Ids where the task could be processed on.
    stage : int
        Number of stage the task should be processed on.
    processing_time : int
        Amount of time the task needs to be processed.
    demands : dict[str, int]
        Dictionary containing all demands of a Task.
        Key: represents the name of the demand
        Value: contains the value of the demand in its defined unit.
        E.g. "energy_demand": 100, "capacity_demand": 2
    """

    task_id: str
    job_id: str
    resource_ids: list[str]
    stage: int
    processing_time: int
    demands: dict[str, int]


class Timespan(BaseModel):
    """
    Contains a start and an end to symbolize a timespan.

    Attributes
    ----------
    start : int
        Start of the time interval.
    end : int
        End of the time interval.
    """

    start: int
    end: int


class Resource(BaseModel):
    """
    A Resource represents a machine that can process a task of a given job.

    Attributes
    ----------
    resource_id : str
        Unique id for the resource.
    stage : int
        Indicates on which stage the machine is positioned.
    transportation_times : dict[str, int] | None
        Dictionary containing all transportation times between existing resources.
        Key: to_machine
        Value: time
    setup_times : dict[str, int] | None
        Dictionary containg setup times.
    teardown_times : dict[str, Timespan] | None
        Dictionary containing teardown times where resource is not available for processing.
    unavailable_times : dict[str, Timespan] | None
        Dictionary containing unavailable times of resource.
    """

    resource_id: str
    stage: int
    transportation_times: dict[str, int] | None  # key = to_machine, value = transportation_time
    setup_times: dict[str, int] | None
    teardown_times: dict[str, Timespan] | None
    unavailable_times: dict[str, Timespan] | None


class Job(BaseModel):
    """
    A Job contains one or more Tasks.

    Attributes
    ----------
    job_id : str
        Unique Id for Job.
    tasks : list[str | list[str]]
        List of tasks containg a list of ?
    due_date : str | None
        Deadline when Job should be done.
    release_time : str | None
        Minimum time when Job has to be released for process.
    """

    job_id: str
    tasks: list[str | list[str]]
    due_date: str | None
    release_time: str | None


class GeneratedProblem(BaseModel):
    """
    Contains the generated Data for the problem with its jobs, tasks and resources.
    """

    tasks: dict[str, Task]
    jobs: dict[str, Job]
    resources: dict[str, Resource]
