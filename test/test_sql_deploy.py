import os
from test.conftest import *

import pytest
from pytest import fail

from src.config import ConfigurationError
from src.fire_classes import run


class TestValidate:
    def test_default_config(self):
        with pytest.raises(ValueError):
            run().validate()

    def test_validate_toml(self):
        with pytest.raises(ValueError):
            run().validate(config="config")

    def test_config_error(self):
        with pytest.raises(SystemExit):
            run().validate(config="config_test.toml")

    def test_config_not_found(self):
        with pytest.raises(FileNotFoundError):
            run().validate(config="test_config_error.toml")


class TestDeploy:
    # def test_default_config(self):
    #     # TODO Get correct connection string for testing
    #     try:
    #         run().deploy()
    #     except ConfigurationError:
    #         pytest.fail("Configuration error")
    #     except ValueError:
    #         pytest.fail("Value error")

    def test_config_error(self):
        with pytest.raises(SystemExit):
            run().deploy(config="test/config_test.toml", connection_string="conn_test")

    def test_ispac(self):
        with pytest.raises(ValueError):
            run().deploy(ispac="test_ispac")
        pass

    def test_ispac_file_exists(self):
        with pytest.raises(FileNotFoundError):
            run().deploy(ispac="test_ispac.ispac")
        pass

    def test_connection_string(self):
        if not os.getenv("CONNECTION_STRING"):
            with pytest.raises(ValueError):
                run().deploy()
        else:
            print("OS connection string available")

    def test_connection_string(self):
        with pytest.raises(ConfigurationError):
            run().deploy(connection_string="conn_test")

    def test_replacement_token(self):

        # TODO Get correct connection string for testing
        run().deploy(
            connection_string="test",
            config="test/config_test.toml",
            replacement_token={"a": "b"},
        )
        # except ConfigurationError:
        #     pytest.fail("Configuration error")
