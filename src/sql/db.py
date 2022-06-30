import datetime
import os

import pyodbc
import sqlparams

from sql import query
from src.exceptions import SqlAgentOperatorException
from src.model import NotifyLevelEmail


class Database:
    def __init__(self, connection_string: str):
        self.connection = pyodbc.connect(connection_string, autocommit=True)
        self.cursor = self.connection.cursor()
        self.sqlparams = sqlparams.SQLParams("named_dollar", "qmark")

    def _execute_sql(self, query: str, parameters: dict, return_results: bool = False):
        # Setting nocount on here means that we don't need to pop it in every one of
        #  our SQL files
        sql, params = self.sqlparams.format(f"SET NOCOUNT ON; {query}", parameters)
        self.cursor.execute(sql, params)
        if return_results:
            return self.cursor.fetchall()

    def _agent_reset_job_step_flow(self, job_name: str):
        self._execute_sql(
            query.agent_reset_job_step_flow,
            {
                "job_name": job_name,
            },
        )

    def _agent_remove_job_alerts(self, job_name: str):
        self._execute_sql(
            query.agent_remove_all_alerts,
            {
                "job_name": job_name,
            },
        )

    def _agent_remove_job_schedules(self, job_name: str):
        self._execute_sql(
            query.agent_remove_all_schedules,
            {
                "job_name": job_name,
            },
        )

    def _agent_remove_job_steps(self, job_name: str):
        self._execute_sql(
            query.agent_remove_all_steps,
            {
                "job_name": job_name,
            },
        )

    def ssis_create_folder(self, folder_name: str):
        self._execute_sql(
            query.ssis_create_folder,
            {
                "folder_name": folder_name,
            },
        )

    def ssis_create_environment(self, environment_name: str, folder_name: str):
        self._execute_sql(
            query.ssis_create_environment,
            {
                "environment_name": environment_name,
                "folder_name": folder_name,
            },
        )

    def ssis_create_environment_reference(
        self, environment_name: str, folder_name: str, project_name: str
    ):
        self._execute_sql(
            query.ssis_create_environment_reference,
            {
                "environment_name": environment_name,
                "folder_name": folder_name,
                "project_name": project_name,
            },
        )

    def ssis_remove_all_environment_variables(
        self, environment_name: str, folder_name: str
    ):
        self._execute_sql(
            query.ssis_remove_all_environment_variables,
            {
                "environment_name": environment_name,
                "folder_name": folder_name,
            },
        )

    def ssis_create_environment_variable(
        self,
        environment_name: str,
        folder_name: str,
        project_name: str,
        variable_name: str,
        variable_value: str,
        is_sensitive: bool = False,
    ):
        self._execute_sql(
            query.ssis_create_environment_variable,
            {
                "environment_name": environment_name,
                "folder_name": folder_name,
                "variable_name": variable_name,
                "variable_value": variable_value,
            },
        )

        self._execute_sql(
            query.ssis_set_environment_reference_to_variable,
            {
                "environment_name": environment_name,
                "folder_name": folder_name,
                "project_name": project_name,
                "variable_name": variable_name,
            },
        )

        if is_sensitive:
            self._execute_sql(
                query.ssis_set_environment_variable_as_sensitive,
                {
                    "environment_name": environment_name,
                    "folder_name": folder_name,
                    "variable_name": variable_name,
                },
            )

    def agent_create_job(
        self, job_name: str, job_description: str, enabled: bool = True
    ):
        self._execute_sql(
            query.agent_create_job,
            {
                "job_name": job_name,
                "job_description": job_description,
                "job_enabled": enabled,
            },
        )

        self._agent_remove_job_alerts(job_name)
        self._agent_remove_job_schedules(job_name)
        self._agent_remove_job_steps(job_name)

    def agent_create_job_step_ssis(
        self,
        job_name: str,
        step_name: str,
        folder_name: str,
        project_name: str,
        ssis_package: str,
        environment_name: str,
        retry_attempts: int,
        retry_interval: int,
        proxy_name: str = None,
    ):
        environment_reference_id = self._execute_sql(
            query.ssis_get_environment_reference_id,
            {
                "project_name": project_name,
                "environment_name": environment_name,
            },
            return_results=True,
        )[0].environment_reference_id

        command = (
            f"""/ISSERVER "\\"\\SSISDB\\{folder_name}\\{project_name}\\{ssis_package}\\"\""""  # noqa
            f""" /SERVER localhost /ENVREFERENCE {environment_reference_id}"""
            """ /Par "\\\"$ServerOption::LOGGING_LEVEL(Int16)\\"\";1"""
            """ /Par "\\\"$ServerOption::SYNCHRONIZED(Boolean)\\"\";True"""
            """ /CALLERINFO"""
            """ SQLAGENT"""
            """ /REPORTING E"""
        )

        if proxy_name:
            self._execute_sql(
                query.agent_create_job_step_using_proxy,
                {
                    "job_name": job_name,
                    "step_name": step_name,
                    "sub_system": "SSIS",
                    "command": command,
                    "database_name": "master",
                    "proxy_name": proxy_name,
                    "retry_attempts": retry_attempts,
                    "retry_interval": retry_interval,
                },
            )
        else:
            self._execute_sql(
                query.agent_create_job_step,
                {
                    "job_name": job_name,
                    "step_name": step_name,
                    "sub_system": "SSIS",
                    "command": command,
                    "database_name": "master",
                    "retry_attempts": retry_attempts,
                    "retry_interval": retry_interval,
                },
            )

        self._agent_reset_job_step_flow(job_name)

    def agent_create_job_step_tsql(
        self,
        job_name: str,
        step_name: str,
        tsql_command: str,
        retry_attempts: int,
        retry_interval: int,
    ):

        self._execute_sql(
            query.agent_create_job_step,
            {
                "job_name": job_name,
                "step_name": step_name,
                "sub_system": "TSQL",
                "command": tsql_command,
                "database_name": "master",
                "retry_attempts": retry_attempts,
                "retry_interval": retry_interval,
            },
        )

        self._agent_reset_job_step_flow(job_name)

    def agent_create_job_schedule_occurs_every_n_minutes(
        self,
        job_name: str,
        schedule_name: str,
        every_n_minutes: int,
        start_time: datetime.time,
    ):
        self._execute_sql(
            query.agent_create_job_schedule,
            {
                "job_name": job_name,
                "schedule_name": schedule_name,
                "occurs_every_n_minutes": every_n_minutes,
                "hh_mm_ss": start_time.strftime("%H%M%S"),
            },
        )

    def ssis_install_ispac(
        self,
        ispac_path: str,
        folder_name: str,
        project_name: str,
    ):
        # The OPENROWSET statement cannot be parameterised, so we have to use token
        # replacement. Before we do this, we should do some sanity checking on the
        # input value first...
        if not ispac_path.endswith(".ispac"):
            raise ValueError("Not an ISPAC file.")

        if not os.path.exists(ispac_path):
            raise FileNotFoundError("Cannot find specific ISPAC file.")

        sql = query.ssis_install_ispac.format(ispac_path=ispac_path)
        self._execute_sql(
            sql,
            {
                "folder_name": folder_name,
                "project_name": project_name,
            },
        )

    def agent_create_operator(self, email_address: str, operator_name: str = None):
        if not operator_name:
            operator_name = email_address

        error_message = self._execute_sql(
            query.agent_create_operator,
            {
                "email_address": email_address,
                "operator_name": operator_name,
            },
            return_results=True,
        )[0].error_message

        if error_message:
            raise SqlAgentOperatorException(error_message)

    def agent_create_notification(
        self,
        job_name: str,
        operator_name: str,
        notify_level_email: int = NotifyLevelEmail.ON_FAILURE.value,
    ):
        error_message = self._execute_sql(
            query.agent_create_notification,
            {
                "job_name": job_name,
                "operator_name": operator_name,
                "notify_level_email": notify_level_email,
            },
            return_results=True,
        )[0].error_message

        if error_message:
            raise SqlAgentOperatorException(error_message)
