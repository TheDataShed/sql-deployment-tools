import copy
import datetime
from test.conftest import TEST_CONFIG

import pytest
import toml
from typing_extensions import assert_type

from src.config import load_configuration
from src.exceptions import ConfigurationError
from src.model import (
    FrequencyInterval,
    FrequencyType,
    NotifyLevelEmail,
    Schedule,
    SsisDeployment,
    Step,
)


class TestFrequencyType:
    def test_FrequencyType_ONCE_equals_1(self):
        """
        Test that FrequencyType.ONCE = 1
        """
        expected = 1

        assert FrequencyType.ONCE.value == expected

    def test_FrequencyType_DAILY_equals_4(self):
        """
        Test that FrequencyType.DAILY = 4
        """
        expected = 4

        assert FrequencyType.DAILY.value == expected

    def test_FrequencyType_WEEKLY_equals_8(self):
        """
        Test that FrequencyType.WEEKLY = 8
        """
        expected = 8

        assert FrequencyType.WEEKLY.value == expected

    def test_FrequencyType_MONTHLY_equals_16(self):
        """
        Test that FrequencyType.MONTHLY = 16
        """
        expected = 16

        assert FrequencyType.MONTHLY.value == expected


class TestFrequencyInterval:
    def test_FrequencyInterval_ONCE_equals_1(self):
        """
        Test that FrequencyInterval.ONCE = 1
        """
        expected = 1

        assert FrequencyInterval.ONCE.value == expected

    def test_FrequencyInterval_DAILY_equals_4(self):
        """
        Test that FrequencyInterval.DAILY = 4
        """
        expected = 4

        assert FrequencyInterval.DAILY.value == expected

    def test_FrequencyInterval_WEEKLY_equals_8(self):
        """
        Test that FrequencyInterval.WEEKLY = 8
        """
        expected = 8

        assert FrequencyInterval.WEEKLY.value == expected


class TestNotifyLevelEmail:
    def test_NotifyLevelEmail_NEVER_equals_0(self):
        """
        Test that NotifyLevelEmail.NEVER = 0
        """
        expected = 0

        assert NotifyLevelEmail.NEVER.value == expected

    def test_NotifyLevelEmail_ON_SUCCESS_equals_1(self):
        """
        Test that NotifyLevelEmail.ON_SUCCESS = 1
        """
        expected = 1

        assert NotifyLevelEmail.ON_SUCCESS.value == expected

    def test_NotifyLevelEmail_ON_FAILURE_equals_2(self):
        """
        Test that NotifyLevelEmail.ON_FAILURE = 2
        """
        expected = 2

        assert NotifyLevelEmail.ON_FAILURE.value == expected

    def test_NotifyLevelEmail_ALWAYS_equals_3(self):
        """
        Test that NotifyLevelEmail.ALWAYS = 3
        """
        expected = 3

        assert NotifyLevelEmail.ALWAYS.value == expected


class TestSsisDeployment:
    def test_SsisDeployment_Project_is_set_correctly(self):
        """
        Test project is set correctly.
        """
        expected = "Bob Ross"
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.project == expected

    def test_SsisDeployment_Folder_is_set_correctly(self):
        """
        Test folder is set correctly.
        """
        expected = "def"
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.folder == expected

    def test_SsisDeployment_Environment_is_set_correctly(self):
        """
        Test environment is set correctly.
        """
        expected = "default"
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.environment == expected

    def test_SsisDeployment_Job_Name_is_set_correctly(self):
        """
        Test job name is set correctly.
        """
        expected = "Season 1 Episode 3"
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.job.name == expected

    def test_SsisDeployment_Job_Description_is_set_correctly(self):
        """
        Test job description is set correctly.
        """
        expected = "Ebony Sunset"
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.job.description == expected

    def test_SsisDeployment_Job_Enabled_Flag_is_set_correctly(self):
        """
        Test job enabled flag is set correctly.
        """
        expected = True
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.job.enabled == expected

    def test_SsisDeployment_Job_Notification_Email_Address_is_set_correctly(self):
        """
        Test notification email address is set correctly.
        """
        expected = "Bob.Ross@thedatashed.co.uk"
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.job.notification_email_address == expected

    def test_SsisDeployment_Number_Job_Steps_is_set_correctly(self):
        """
        Test number of job steps is correct.
        """
        expected = 2
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert len(actual.job.steps) == expected

    def test_SsisDeployment_Job_Steps_are_set_correctly(self):
        """
        Test job steps are correct.
        """
        expected = [
            Step("Season 1 Episode 4", "SSIS", "WinterMist.dtsx"),
            Step("Season 1 Episode 5", "SSIS", "QuietStream.dtsx"),
        ]
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.job.steps == expected

    def test_SsisDeployment_Number_Job_Schedules_is_set_correctly(self):
        """
        Test number of job schedules is correct.
        """
        expected = 2
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert len(actual.job.schedules) == expected

    def test_SsisDeployment_Job_Schedules_are_set_correctly(self):
        """
        Test job schedules are set correctly.
        """
        expected = [
            Schedule("Winter Moon", 30, datetime.time(0, 0)),
            Schedule("Autumn Mountain", 1440, datetime.time(0, 0)),
        ]
        actual = load_configuration(toml.dumps(TEST_CONFIG))
        assert actual.job.schedules == expected

    def test_SsisDeployment_job_step_count_is_set_correctly(self):
        """
        Test the correct number of job steps are set.
        """
        expected = 2
        actual = len(load_configuration(toml.dumps(TEST_CONFIG)).job.steps)
        assert actual == expected

    def test_SsisDeployment_job_schedule_count_is_set_correctly(self):
        """
        Test the correct number of job schedules are set.
        """
        expected = 2
        actual = len(load_configuration(toml.dumps(TEST_CONFIG)).job.schedules)
        assert actual == expected

    def test_SsisDeployment_parameter_count_is_set_correctly(self):
        """
        Test the correct number of parameters are set.
        """
        expected = 2
        actual = len(load_configuration(toml.dumps(TEST_CONFIG)).parameters)
        assert actual == expected

    def test_SsisDeployment_throws_an_exception_when_project_name_is_not_set(self):
        """
        Test project is not optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["project"] = None

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_throws_an_exception_when_project_is_not_in_config(self):
        """
        Test project is not optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        del config["project"]

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_throws_an_exception_when_folder_is_not_set(self):
        """
        Test folder is not optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["folder"] = None

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_throws_an_exception_when_folder_is_in_config(self):
        """
        Test folder is not optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        del config["folder"]

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_environment_is_optional(self):
        """
        Test environment is optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["environment"] = None

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    def test_SsisDeployment_does_not_error_when_no_parameters_are_present_in_config(
        self,
    ):
        """
        Test parameters are optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        del config["parameters"]

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    def test_SsisDeployment_does_not_error_when_parameters_is_empty(self):
        """
        Test parameters are optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["parameters"] = []

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    def test_SsisDeployment_errors_when_job_is_not_present_in_config(self):
        """
        Test that job is not optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        del config["job"]

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_errors_when_job_name_is_not_set(self):
        """
        Test that job name is not optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["job"] = {}

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_does_not_error_when_job_steps_are_not_present_in_config(
        self,
    ):
        """
        Test that job steps are optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        del config["job"]["steps"]

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    def test_SsisDeployment_does_not_error_when_job_steps_is_empty(self):
        """
        Test that job steps are optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["job"]["steps"] = []

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    def test_SsisDeployment_does_not_error_when_job_schedules_are_not_present_in_config(
        self,
    ):
        """
        Test that job schedules are optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        del config["job"]["schedules"]

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    def test_SsisDeployment_does_not_error_when_job_schedules_is_empty(self):
        """
        Test that job schedules are optional.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["job"]["schedules"] = []

        assert_type(load_configuration(toml.dumps(config)), SsisDeployment)

    @pytest.mark.skip("George needs to implement Pydantic models :)")
    def test_SsisDeployment_throws_an_exception_when_schedule_minutes_is_not_an_integer(
        self,
    ):
        """
        Test job schedule interval cannot be anything other than an integer.
        """
        config = copy.deepcopy(TEST_CONFIG)
        config["job"]["schedules"][0][
            "every_n_minutes"
        ] = "No mistakes, just happy little accidents"

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_throws_exception_step_type_is_ssis_tsql_command_set(
        self,
    ):
        """
        Test that if job_step type is set to SSIS but a
        SQL String is provided that the config fails.
        """

        config = copy.deepcopy(TEST_CONFIG)
        del config["job"]["steps"][0]["ssis_package"]
        config["job"]["steps"][0]["tsql_command"] = "SELECT 1 AS n"

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_throws_exception_step_type_is_tsql_ssis_package_set(
        self,
    ):
        """
        Test that if job_step type is set to T-SQL
        but a ssis_package is provided that the config fails.
        """

        config = copy.deepcopy(TEST_CONFIG)
        config["job"]["steps"][0]["type"] = "T-SQL"

        with pytest.raises(ConfigurationError):
            load_configuration(toml.dumps(config))

    def test_SsisDeployment_does_not_throw_exception_step_tsql_command_provided(
        self,
    ):
        """
        Test that the config is valid when job step
        is t-sql and tsql_command is provided.
        """

        config = copy.deepcopy(TEST_CONFIG)
        config["job"]["steps"][0]["type"] = "T-SQL"
        del config["job"]["steps"][0]["ssis_package"]
        config["job"]["steps"][0]["tsql_command"] = "SELECT 1 AS number"

        actual = load_configuration(toml.dumps(config))
        assert_type(actual, SsisDeployment)
