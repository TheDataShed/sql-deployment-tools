import toml

from exceptions import ConfigurationError
from model import SsisDeployment


def load_configuration(configuration: str) -> SsisDeployment:
    try:
        config = toml.loads(configuration)
        return SsisDeployment.from_dict(config)
    except Exception as ex:
        raise ConfigurationError(ex)
