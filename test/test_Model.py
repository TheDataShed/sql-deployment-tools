import datetime
from cmath import exp
from json import load
from test.conftest import *

import pytest
import this
from pytest import fail
from typing_extensions import assert_type

from src.config import *
from src.model import *


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
        expected = "Bob Ross"
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.project == expected

    def test_SsisDeployment_Folder_is_set_correctly(self):
        expected = "def"
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.folder == expected

    def test_SsisDeployment_Environment_is_set_correctly(self):
        expected = "default"
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.environment == expected

    def test_SsisDeployment_Job_Name_is_set_correctly(self):
        expected = "whatever"
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.job.name == expected

    def test_SsisDeployment_Job_Description_is_set_correctly(self):
        expected = "cool"
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.job.description == expected

    def test_SsisDeployment_Job_Enabled_Flag_is_set_correctly(self):
        expected = True
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.job.enabled == expected

    def test_SsisDeployment_Job_Notification_Email_Address_is_set_correctly(self):
        expected = "Bob.Ross@thedatashed.co.uk"
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.job.notification_email_address == expected

    def test_SsisDeployment_Number_Job_Steps_is_set_correctly(self):
        expected = 2
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert len(actual.job.steps) == expected

    def test_SsisDeployment_Job_Steps_are_set_correctly(self):
        expected = [
            Step("todo", "SSIS", "Package1.dtsx"),
            Step("Paint mountain scene", "SSIS", "PaintRivers.dtsx"),
        ]
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert actual.job.steps == expected

    def test_SsisDeployment_Number_Job_Schedules_is_set_correctly(self):
        expected = 2
        actual = load_configuration(get_config_text(VALID_CONFIG))
        assert len(actual.job.schedules) == expected

    def test_SsisDeployment_Job_Schedules_are_set_correctly(self):
        expected = [
            Schedule("name1", 12, datetime.time(0, 0)),
            Schedule("name2", 111, datetime.time(0, 0)),
        ]
        actual = load_configuration(get_config_text(VALID_CONFIG))
        print(actual)
        assert actual.job.schedules == expected
