from test.conftest import *

import pytest
from pytest import fail

from src.fire_classes import run


class TestValidate:
    def test_validate_toml(self):
        with pytest.raises(ValueError):
            run().validate(config="config")
