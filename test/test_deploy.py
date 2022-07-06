import pytest

from src.deploy import deploy_ssis
from src.model import SsisDeployment, Job, Parameter

import pytest
import unittest.mock


@pytest.fixture()
def mock_database():
    with unittest.mock.patch("src.deploy.Database") as mock_database:
        yield mock_database


def test_deploy_ssis_folder_created(mock_database):
    deploy_ssis(
        connection_string="mock_connection_string",
        ispac_path=None,
        ssis_deployment=SsisDeployment(
            project="Project Teeling",
            folder="origami",
        ),
    )
    mock_database.return_value.ssis_create_folder.assert_called_once_with(
        folder_name="origami"
    )


def test_deploy_ispac(mock_database):
    deploy_ssis(
        connection_string="mock_connection_string",
        ispac_path="/path/to/file.ispac",
        ssis_deployment=SsisDeployment(
            project="Project Scapa",
            folder="wood",
        ),
    )
    mock_database.return_value.ssis_install_ispac.assert_called_once_with(
        ispac_path="/path/to/file.ispac",
        folder_name="wood",
        project_name="Project Scapa",
    )


def test_deploy_without_ispac(mock_database):
    deploy_ssis(
        connection_string="mock_connection_string",
        ispac_path=None,
        ssis_deployment=SsisDeployment(project="Project Scapa", folder="wood"),
    )
    mock_database.return_value.ssis_install_ispac.assert_not_called()


def test_deploy_ssis_default_environment(mock_database):
    deploy_ssis(
        connection_string="mock_connection_string",
        ispac_path=None,
        ssis_deployment=SsisDeployment(
            project="Project Auchentoshan",
            folder="paper",
        ),
    )
    mock_database.return_value.ssis_create_environment.assert_called_once_with(
        environment_name="default", folder_name="paper"
    )
    mock_database.return_value.ssis_create_environment_reference.assert_called_once_with(
        environment_name="default",
        folder_name="paper",
        project_name="Project Auchentoshan",
    )
    mock_database.return_value.ssis_remove_all_environment_variables.assert_called_once_with(
        environment_name="default", folder_name="paper"
    )


def test_deploy_ssis_specific_environment(mock_database):
    deploy_ssis(
        connection_string="mock_connection_string",
        ispac_path=None,
        ssis_deployment=SsisDeployment(
            project="Project Raasay", folder="plastic", environment="cobalt"
        ),
    )
    mock_database.return_value.ssis_create_environment.assert_called_once_with(
        environment_name="cobalt", folder_name="plastic"
    )
    mock_database.return_value.ssis_create_environment_reference.assert_called_once_with(
        environment_name="cobalt",
        folder_name="plastic",
        project_name="Project Raasay",
    )
    mock_database.return_value.ssis_remove_all_environment_variables.assert_called_once_with(
        environment_name="cobalt", folder_name="plastic"
    )


def test_deploy_ssis_single_parameter(mock_database):
    deploy_ssis(
        connection_string="mock_connection_string",
        ispac_path=None,
        ssis_deployment=SsisDeployment(
            project="Project Raasay", folder="plastic", parameters=[
                Parameter(name="foo", value="bar"),
            ]
        ),
    )
    # mock_database.return_value.ssis_create_environment_variable
