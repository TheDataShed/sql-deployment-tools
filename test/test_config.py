from test.conftest import TEST_CONFIG

import pytest
import toml
from typing_extensions import assert_type

from config import load_configuration
from exceptions import ConfigurationError
from model import SsisDeployment


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

        with pytest.raises(Exception):
            load_configuration(tomlConfig)
