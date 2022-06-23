import toml

from src.model import SsisDeployment


class ConfigurationError(Exception):
    pass


def load_configuration(configuration: str) -> SsisDeployment:
    try:
        config = toml.loads(configuration)
        return SsisDeployment.from_dict(config)
    except Exception as ex:
        raise ConfigurationError(ex)
