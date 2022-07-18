import datetime
import typing
from dataclasses import dataclass, field
from enum import Enum

from dataclasses_json import config, dataclass_json

from src.exceptions import ConfigurationError


class FrequencyType(Enum):
    ONCE = 1
    DAILY = 4
    WEEKLY = 8
    MONTHLY = 16


class FrequencyInterval(Enum):
    ONCE = 1
    DAILY = 4
    WEEKLY = 8


class NotifyLevelEmail(Enum):
    NEVER = 0
    ON_SUCCESS = 1
    ON_FAILURE = 2
    ALWAYS = 3


class UnitTypeFrequencyType(Enum):
    MINUTE = 4
    DAY = 4

class UnitTypeFrequencyInterval(Enum):
    MINUTE = 1
    DAY = 4


@dataclass
class Parameter:
    name: str
    value: str
    sensitive: bool = False


@dataclass_json
@dataclass
class Schedule:
    name: str
    unit: str
    every_n_units: int
    schedule_time: str = "000000"


@dataclass
class Step:
    name: str
    _type: str = field(metadata=config(field_name="type"))
    ssis_package: typing.Optional[str] = None
    tsql_command: typing.Optional[str] = None
    retry_attempts: typing.Optional[int] = 0
    retry_interval: typing.Optional[int] = 0
    proxy: typing.Optional[str] = None

    def __post_init__(self):
        if self._type == "SSIS" and not self.ssis_package:
            raise ConfigurationError("'ssis_package must be provided.'")
        elif self._type == "T-SQL" and not self.tsql_command:
            raise ConfigurationError("'tsql_command' must be provided.")


@dataclass
class Job:
    name: str
    description: str = ""
    steps: typing.List[Step] = field(default_factory=list)
    schedules: typing.List[Schedule] = field(default_factory=list)
    enabled: bool = True
    notification_email_address: typing.Optional[str] = None


@dataclass_json
@dataclass
class SsisDeployment:
    project: str
    folder: str
    job: Job = field(default_factory=dict)
    parameters: typing.List[Parameter] = field(default_factory=list)
    environment: str = "default"
