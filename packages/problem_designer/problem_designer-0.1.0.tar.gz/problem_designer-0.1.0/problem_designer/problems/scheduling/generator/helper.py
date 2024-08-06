import math
from dataclasses import dataclass

import numpy as np

from problem_designer.problems.scheduling.constants.characteristic import (
    DemandsCharacteristics,
    ProcessingTimeCharacteristic,
    TransportationTimeCharacteristic,
)
from problem_designer.problems.scheduling.constants.objective import SupportedObjectives
from problem_designer.problems.scheduling.generator.typedef import (
    GeneratorStep,
    IntermediateGeneratedProblem,
)


@dataclass
class GenerateFixedNumberOfTasksPerJob(GeneratorStep):
    """
    Generates a mapping for a job containing a fixed number of tasks
    """

    number_of_jobs: int
    number_of_tasks_per_job: int

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.map_job_to_task_count = {f"{job_id}": self.number_of_tasks_per_job for job_id in range(self.number_of_jobs)}
        igp.number_of_jobs = self.number_of_jobs
        igp.total_number_of_tasks = sum(igp.map_job_to_task_count.values())
        return igp


@dataclass
class GenerateAmountOfStages(GeneratorStep):
    """
    Generates the amount of stages
    """

    number_of_stages: int

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.number_of_stages = self.number_of_stages
        return igp


@dataclass
class GenerateFixedIndexMappingToMachine(GeneratorStep):
    """
    Generates a fixed mapping from the ith task to the ith machine
    """

    number_of_machines: int

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        task_to_machine_mapper = {}
        for job_index in igp.map_job_to_task_count.keys():
            number_of_tasks = igp.map_job_to_task_count[job_index]

            # generate mapping
            mapping = list(np.linspace(start=0, stop=number_of_tasks - 1, num=number_of_tasks, dtype=int))
            task_to_machine_mapper[job_index] = mapping
        igp.map_machine_to_task = task_to_machine_mapper
        igp.number_of_machines = self.number_of_machines
        return igp


@dataclass
class GenerateFixedIndexMappingFromStageToMachine(GeneratorStep):
    """
    Generates a fixed mapping from stage to machine
    """

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.number_of_machines_per_stage = int(igp.number_of_machines / igp.number_of_stages)
        stage_to_machine_mapper = {}
        counter = 0
        for stage in range(igp.number_of_stages):
            mapping = list(range(counter, counter + igp.number_of_machines_per_stage))
            counter = counter + igp.number_of_machines_per_stage
            stage_to_machine_mapper[str(stage)] = mapping
        igp.map_stage_to_machine = stage_to_machine_mapper
        return igp


@dataclass
class GenerateProcessingTimes(GeneratorStep):
    """
    Generates processing times according to a distribution
    """

    pt: ProcessingTimeCharacteristic

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        job_to_processing_times = {}
        for job_index in igp.map_job_to_task_count.keys():
            job_to_processing_times[job_index] = self.pt.distribution.take_n(n=igp.map_job_to_task_count[job_index])
        igp.job_to_processing_times = job_to_processing_times
        return igp


@dataclass
class GenerateTransportationTimesForMachinesWithStages(GeneratorStep):
    """
    Generates transportation times between two machines at two different stages according to a distribution
    """

    tt: TransportationTimeCharacteristic

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        machine_to_transportation_times = {}
        for stage, machines in igp.map_stage_to_machine.items():
            for machine in machines:
                next_stage_dict = {}
                next_stage = int(stage) + 1
                # check if next stage exists
                if next_stage < len(igp.map_stage_to_machine):
                    next_stage_machines = igp.map_stage_to_machine[str(next_stage)]
                    for next_machine in next_stage_machines:
                        next_stage_dict[str(next_machine)] = self.tt.distribution.get_random_value()
                else:
                    next_stage_dict = None
                machine_to_transportation_times[str(machine)] = next_stage_dict
        igp.machine_to_transportation_times = machine_to_transportation_times
        return igp


@dataclass
class GenerateTransportationTimes(GeneratorStep):
    """
    Generates transportation times between two machines according to a distribution
    """

    tt: TransportationTimeCharacteristic

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        list_of_dicts = []
        for m in range(igp.number_of_machines):
            machine_to_transportation_times = {}
            for n in range(igp.number_of_machines):
                machine_to_transportation_times[str(n)] = self.tt.distribution.get_random_value()
            list_of_dicts.append(machine_to_transportation_times)
        igp.machine_to_transportation_times = list_of_dicts
        return igp


@dataclass
class GenerateMachineCapacities(GeneratorStep):
    """
    Generates capacities for every machine for given time stamps.
    If no value for capacity is given, default value 1 is taken.
    Dictionary structure: { "machine_id": { "time_stamp": capacity } }
    """

    cp: dict[str, dict[str, int]]
    default_cap: int | dict[str, int]

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        # set default capacities
        if type(self.default_cap) is int:
            # self.default_cap = [self.default_cap] * igp.number_of_machines
            temp = {}
            # create dict instead of list
            for i in range(igp.number_of_machines):
                temp[str(i)] = self.default_cap
            self.default_cap = temp
        elif type(self.default_cap) is dict:
            while len(self.default_cap) < igp.number_of_machines:
                # if not enough capacities are given, append 1 as default capacity
                self.default_cap[str(len(self.default_cap))] = 1
        igp.default_capacities = self.default_cap

        # if there are less capacities given than there are machines add empty dicts
        while len(self.cp) < igp.number_of_machines:
            self.cp[str(len(self.cp))] = {}
        igp.machine_capacity = self.cp
        return igp


@dataclass
class GenerateDemands(GeneratorStep):
    """
    Generates capacity and energy demands according to a distribution.
    Dictionary structure: { "task_id": { "demand_type": value } }
    """

    dc: DemandsCharacteristics

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        demands = {}
        for task in range(igp.total_number_of_tasks):
            energy_demand = self.dc.distribution.take_one()
            demands[str(task)] = {
                "capacity_demand": 1,
                # round up to next 100
                "energy_demand": int(math.ceil(energy_demand / 100)) * 100,
            }
        igp.demands = demands
        return igp


@dataclass
class GenerateObjectives(GeneratorStep):
    objectives: list[SupportedObjectives]

    def generate(self, igp: IntermediateGeneratedProblem) -> IntermediateGeneratedProblem:
        igp.objectives = [o.type for o in self.objectives]
        return igp
