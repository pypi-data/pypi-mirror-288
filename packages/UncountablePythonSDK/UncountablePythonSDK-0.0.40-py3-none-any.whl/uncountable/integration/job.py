from abc import ABC, abstractmethod
from dataclasses import dataclass

from uncountable.core.client import Client
from uncountable.integration.types import JobDefinition


@dataclass
class JobArgumentsBase:
    job_definition: JobDefinition
    client: Client


@dataclass
class CronJobArguments(JobArgumentsBase):
    # can imagine passing additional data such as in the sftp or webhook cases
    pass


JobArguments = CronJobArguments


@dataclass
class JobResult:
    success: bool


class Job(ABC):
    _unc_job_registered: bool = False

    @abstractmethod
    def run(self, args: JobArguments) -> JobResult: ...


class CronJob(Job):
    @abstractmethod
    def run(self, args: CronJobArguments) -> JobResult: ...


def register_job(cls: Job) -> Job:
    cls._unc_job_registered = True
    return cls
