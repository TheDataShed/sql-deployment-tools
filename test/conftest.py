import os
import sys

import pytest

_ROOT = os.path.dirname(__file__)
VALID_CONFIG = "config_templates/valid_config.toml"
INVALID_CONFIG = "config_templates/invalid_config.toml"


def get_config_text(path):
    if not path:
        raise Exception("path cannot be null or empty.")

    with open(os.path.join(_ROOT, path)) as file:
        return file.read()
