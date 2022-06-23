import os
import sys

import fire

from config import ConfigurationError, load_configuration
from deploy import deploy_ssis
from model import SsisDeployment


class run:
    def validate(self, config="config.toml"):
        configuration = open(config, "r").read()
        if not self.config.endswith(".toml"):
            raise ValueError(f"Config must be a TOML file.")

        try:
            load_configuration(configuration)
        except ConfigurationError:
            sys.exit("Invalid configuration.")

    def deploy(
        self,
        config="config.toml",
        ispac=None,
        connection_string=None,
        replacement_token=None,
    ):
        """Deploy \n
        Deploy SSIS based on the configuration \n
        --config: TOML configuration file (default: config.toml) \n
        --ispac Path to `*.ispac` file to be deployed \n
        --connection-string Connection string. If not supplied we'll attempt to use environment variable `CONNETION_STRING` \n
        --replacement-tokens Variables to be replaced in the TOML file
        """

        configuration = open(config, "r").read()
        if ispac:
            if not ispac.endswith(".ispac"):
                raise ValueError(f"Not an ISPAC file.")

            if not os.path.exists(ispac):
                raise FileNotFoundError("Cannot find specific ISPAC file.")

        connection_string = connection_string or os.getenv("CONNECTION_STRING")
        if not connection_string:
            raise ValueError(
                "Missing connection string. Can either be supplied using the `--connection-string` argument or via an environment variable `CONNETION_STRING`"
            )

        if replacement_token:
            configuration = configuration.format(**replacement_token)

        ssis_deployment = load_configuration(configuration)
        deploy_ssis(connection_string, ispac, ssis_deployment)


if __name__ == "__main__":
    fire.Fire(run)
