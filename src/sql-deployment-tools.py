import argparse
import json
import os
import sys

from config import ConfigurationError, load_configuration
from deploy import deploy_ssis
from model import SsisDeployment

if __name__ == "__main__":
    parent_parser = argparse.ArgumentParser(description="SSIS Deployment Helper")

    subparsers = parent_parser.add_subparsers(help="sub-command help", dest="command")

    validate = subparsers.add_parser("validate", help="Validate the config file")
    validate.add_argument(
        "--config",
        help="TOML configuration file (default: config.toml)",
        type=argparse.FileType("r"),
        default="config.toml",
        required=False,
    )

    deploy = subparsers.add_parser(
        "deploy", help="Deploy SSIS based on the configuration"
    )
    deploy.add_argument(
        "--config",
        help="TOML configuration file (default: config.toml)",
        type=argparse.FileType("r"),
        default="config.toml",
        required=False,
    )
    deploy.add_argument(
        "--ispac",
        type=str,
        help="Path to `*.ispac` file to be deployed.",
        required=False,
    )
    deploy.add_argument(
        "--connection-string",
        type=str,
        help="Connection string. If not supplied we'll attempt to use environment variable `CONNETION_STRING`",
        required=False,
    )
    deploy.add_argument(
        "--replacement-tokens",
        type=json.loads,
        help="Variables to be replaced in the TOML file",
        required=False,
    )

    args = parent_parser.parse_args()

    if not args.config.name.endswith(".toml"):
        raise ValueError(f"Config must be a TOML file.")

    configuration = args.config.read()
    args.config.close()

    if args.command == "validate":
        try:
            load_configuration(configuration)
        except ConfigurationError:
            sys.exit("Invalid configuration.")
    elif args.command == "deploy":
        if args.ispac:
            if not args.ispac.endswith(".ispac"):
                raise ValueError(f"Not an ISPAC file.")

            if not os.path.exists(args.ispac):
                raise FileNotFoundError("Cannot find specific ISPAC file.")

        connection_string = args.connection_string or os.getenv("CONNECTION_STRING")
        if not connection_string:
            raise ValueError(
                "Missing connection string. Can either be supplied using the `--connection-string` argument or via an environment variable `CONNETION_STRING`"
            )

        if args.replacement_tokens:
            configuration = configuration.format(**args.replacement_tokens)

        ssis_deployment = load_configuration(configuration)
        deploy_ssis(connection_string, args.ispac, ssis_deployment)

    else:
        raise NotImplementedError(f"Command not supported: {args.command}")
