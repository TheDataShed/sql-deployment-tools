import os
from test.conftest import *

import pyodbc
import pytest
from pytest import fail

from src.config import ConfigurationError
from src.fire_classes import run


class TestValidate:
    def test_validate_toml(self):
        with pytest.raises(ValueError):
            run().validate(config="config")

    def test_config_error(self):
        with pytest.raises(SystemExit):
            run().validate(config="test/test_config_error.toml")

    def test_config_not_found(self):
        with pytest.raises(FileNotFoundError):
            run().validate(config="test_config_error.toml")


class TestDeploy:
    def test_config_error(self):
        with pytest.raises(ConfigurationError):
            run().deploy(
                config="test/test_config_error.toml", connection_string="conn_test"
            )

    def test_ispac(self):
        with pytest.raises(ValueError):
            run().deploy(ispac="test_ispac", config="test/test_config.toml")

    def test_ispac_file_exists(self):
        with pytest.raises(FileNotFoundError):
            run().deploy(ispac="test/test_ispac.ispac", config="test/test_config.toml")

    def test_connection_string(self):
        if not os.getenv("CONNECTION_STRING"):
            with pytest.raises(ValueError):
                run().deploy(config="test/test_config.toml")
        else:
            print("OS connection string available")

    def test_connection_string(self):
        with pytest.raises(ConfigurationError):
            run().deploy(connection_string="conn_test")

    def test_replacement_token(self):
        try:
            run().deploy(
                connection_string="test",
                config="test/config_test_replacement_token.toml",
                replacement_token={"value": "test", "email": "test"},
            )
        except KeyError:
            pytest.fail("KeyError: token not found in config")
        except pyodbc.InterfaceError:
            pass

    def test_replacement_token_error(self):
        with pytest.raises(KeyError):
            run().deploy(
                connection_string="test",
                config="test/config_test_replacement_token.toml",
                replacement_token={"test": "test", "email": "test"},
            )
