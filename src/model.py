import datetime
import typing
from dataclasses import dataclass, field
from enum import Enum

from dataclasses_json import config, dataclass_json


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


@dataclass
class Parameter:
    name: str
    value: str
    sensitive: bool = False


@dataclass_json
@dataclass
class Schedule:
    name: str
    every_n_minutes: int
    start_time: datetime.time = field(
        default=datetime.time(hour=0, minute=0, second=0),
        metadata=config(decoder=datetime.time.fromisoformat),
    )


@dataclass
class Step:
    name: str
    _type: str = field(metadata=config(field_name="type"))
    package: str
    proxy: typing.Optional[str] = None


@dataclass
class Job:
    name: str
    description: str
    steps: typing.List[Step]
    schedules: typing.List[Schedule]
    enabled: bool = True
    notification_email_address: typing.Optional[str] = None


@dataclass_json
@dataclass
class SsisDeployment:
    project: str
    folder: str
    job: Job
    parameters: typing.List[Parameter]
    environment: str = "default"
