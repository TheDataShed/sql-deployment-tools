from src.exceptions import SqlAgentOperatorException
from src.model import SsisDeployment
from src.sql.db import Database


def deploy_ssis(
    connection_string: str, ispac_path: str, ssis_deployment: SsisDeployment
):
    db = Database(connection_string)

    project_name = ssis_deployment.project
    folder_name = ssis_deployment.folder
    environment_name = ssis_deployment.environment

    db.ssis_create_folder(folder_name)

    if ispac_path:
        db.ssis_install_ispac(ispac_path, folder_name, project_name)

    db.ssis_create_environment(environment_name, folder_name)
    db.ssis_create_environment(environment_name, folder_name)
    db.ssis_create_environment_reference(environment_name, folder_name, project_name)
    db.ssis_remove_all_environment_variables(environment_name, folder_name)

    for parameter in ssis_deployment.parameters:
        db.ssis_create_environment_variable(
            environment_name=environment_name,
            folder_name=folder_name,
            project_name=project_name,
            variable_name=parameter.name,
            variable_value=parameter.value,
            is_sensitive=parameter.sensitive,
        )


def deploy_agent_job(connection_string: str, agent_deployment: SsisDeployment):

    db = Database(connection_string)

    job_name = agent_deployment.job.name
    job_description = agent_deployment.job.description
    folder_name = agent_deployment.folder if agent_deployment.folder else None
    project_name = agent_deployment.project if agent_deployment.project else None
    environment = agent_deployment.environment if agent_deployment.environment else None

    db.agent_create_job(job_name, job_description)

    for job_step in agent_deployment.job.steps:

        if job_step._type not in ["SSIS", "T-SQL"]:

            raise NotImplementedError(
                """Only job.steps.type==SSIS and
                job.steps.type==T-SQL are currently supported"""
            )

        if job_step._type == "SSIS":
            db.agent_create_job_step_ssis(
                job_name,
                job_step.name,
                folder_name,
                project_name,
                job_step.ssis_package,
                environment,
                job_step.retry_attempts,
                job_step.retry_interval,
                job_step.proxy,
            )

        if job_step._type == "T-SQL":
            db.agent_create_job_step_tsql(
                job_name,
                job_step.name,
                job_step.tsql_command,
                job_step.retry_attempts,
                job_step.retry_interval,
            )

    for job_schedule in agent_deployment.job.schedules:
        db.agent_create_job_schedule_occurs_every_n_minutes(
            job_name,
            job_schedule.name,
            job_schedule.every_n_minutes,
            job_schedule.start_time,
        )

    if agent_deployment.job.notification_email_address:
        try:
            db.agent_create_operator(agent_deployment.job.notification_email_address)
        except SqlAgentOperatorException as ex:
            # TODO: log a warning properly, not just print the message
            print(ex)

        try:
            db.agent_create_notification(
                job_name, agent_deployment.job.notification_email_address
            )
        except SqlAgentOperatorException as ex:
            # TODO: log a warning properly, not just print the message
            print(ex)
