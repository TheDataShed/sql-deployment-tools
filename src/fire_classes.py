import fire
import os
import sys

from config import ConfigurationError, load_configuration
from deploy import deploy_ssis
from model import SsisDeployment

class validate():
    """Deploy \n
        Deploy SSIS based on the configuration \n
        --config: TOML configuration file (default: config.toml) \n
    """
    def __init__(self, config="config.toml"):
        self.config = config
    


class run():
    """Deploy \n
        Deploy SSIS based on the configuration \n
        --config: TOML configuration file (default: config.toml) \n
        --ispac Path to `*.ispac` file to be deployed \n
        --connection-string Connection string. If not supplied we'll attempt to use environment variable `CONNETION_STRING` \n
        --replacement-tokens Variables to be replaced in the TOML file
    """
    # def __init__(self):
        # self.config = config
        # self.ispac = ispac
        # self.connection_string = connection_string
        # self.replacement_token = replacement_token
    
    def validate(self, config="config.toml"):
        self.config = config
        configuration = open(self.config, "r").read()
        if not self.config.endswith(".toml"):
            raise ValueError(f"Config must be a TOML file.")
        
        try:
            load_configuration(configuration)
        except ConfigurationError:
            sys.exit("Invalid configuration.")
        
    
    def deploy(self, config="config.toml", ispac=None, connection_string=None, replacement_token=None):
        self.config = config
        self.ispac = ispac
        self.connection_string = connection_string
        self.replacement_token = replacement_token
        
        configuration = open(self.config, "r").read()
        if self.ispac:
            print(self.ispac, self.config)
            if not self.ispac.endswith(".ispac"):
                raise ValueError(f"Not an ISPAC file.")

            if not os.path.exists(self.ispac):
                raise FileNotFoundError("Cannot find specific ISPAC file.")

        connection_string = self.connection_string or self.getenv("CONNECTION_STRING")
        if not connection_string:
            raise ValueError(
                "Missing connection string. Can either be supplied using the `--connection-string` argument or via an environment variable `CONNETION_STRING`"
            )

        if self.replacement_token:
            configuration = configuration.format(**self.replacement_token)

        ssis_deployment = load_configuration(configuration)
        deploy_ssis(connection_string, self.ispac, ssis_deployment)
        
if __name__ == '__main__':
  # calculator = replacement_tokens()
  fire.Fire(run)
