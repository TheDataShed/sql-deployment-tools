import os
import sys
from json import load
from test.conftest import *

import pytest
from pytest import fail
from typing_extensions import assert_type

from src.config import *
from src.model import *


class TestConfig:
    def test_valid_configuration_loads(self):
        """
        Test that a valid configuration returns a 'SsisDeployment' object.
        """
        tomlConfig = toml.dumps(TEST_CONFIG)

        assert_type(load_configuration(tomlConfig), SsisDeployment)

    def test_invalid_configuration_does_not_load(self):
        """
        Test that an invalid configuration raises an exception.
        """
        tomlConfig = toml.dumps("")

        with pytest.raises(ConfigurationError):
            load_configuration(tomlConfig)
