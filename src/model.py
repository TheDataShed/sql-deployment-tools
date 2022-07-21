import datetime
import typing
from dataclasses import dataclass, field
from enum import Enum

from dataclasses_json import config, dataclass_json

from exceptions import ConfigurationError


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
    WEEK = 8
    MONTH = 16


class DayOfWeekFrequencyInterval(Enum):
    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 4
    WEDNESDAY = 8
    THURSDAY = 16
    FRIDAY = 32
    SATURDAY = 64


@dataclass
class Parameter:
    name: str
    value: str
    sensitive: bool = False


@dataclass
class ScheduleQueryParameters:
    freq_type: int
    freq_interval: int
    freq_subday_type: int
    freq_subday_interval: int
    freq_recurrence_factor: int
    active_start_time: int


@dataclass_json
@dataclass
class Schedule:
    name: str
    unit: str
    every_n_units: int
    schedule_time: int = 0
    run_days: typing.Optional[typing.List[str]] = None
    day_of_month: typing.Optional[int] = None

    def transform_for_query(self) -> ScheduleQueryParameters:
        if self.unit == "MINUTE":
            return ScheduleQueryParameters(
                UnitTypeFrequencyType.MINUTE.value,
                1,
                4,
                self.every_n_units,
                0,
                self.schedule_time
            )
        if self.unit == "DAY":
            return ScheduleQueryParameters(
                UnitTypeFrequencyType.DAY.value,
                self.every_n_units,
                1,
                0,
                0,
                self.schedule_time
            )
        if self.unit == "WEEK":
            return ScheduleQueryParameters(
                UnitTypeFrequencyType.WEEK.value,
                sum([DayOfWeekFrequencyInterval[x].value for x in self.run_days]),
                1,
                0,
                self.every_n_units,
                self.schedule_time
            )
        if self.unit == "MONTH":
            return ScheduleQueryParameters(
                UnitTypeFrequencyType.MONTH.value,
                self.day_of_month,
                1,
                0,
                self.every_n_units,
                self.schedule_time
            )
    
    def __post_init__(self):
        if self.unit == "WEEK" and not self.run_days:
            raise ConfigurationError("'run_days must be provided.'")
        elif self.unit == "MONTH" and not self.day_of_month:
            raise ConfigurationError("'day_of_month must be provided.'")


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
