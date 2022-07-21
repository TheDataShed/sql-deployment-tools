from exceptions import SqlAgentOperatorException
from model import SsisDeployment
from sql.db import Database


def deploy_ssis(
    connection_string: str, ispac_path: str, ssis_deployment: SsisDeployment
):
    db = Database(connection_string)

    project_name = ssis_deployment.project
    folder_name = ssis_deployment.folder
    environment_name = ssis_deployment.environment
    job_name = ssis_deployment.job.name
    job_description = ssis_deployment.job.description

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

    db.agent_create_job(job_name, job_description)

    for job_step in ssis_deployment.job.steps:

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
                environment_name,
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

    for job_schedule in ssis_deployment.job.schedules:
        parameters = job_schedule.transform_for_query()
        db.agent_create_job_schedule(
            job_name,
            job_schedule.name,
            parameters.freq_type,
            parameters.freq_interval,
            parameters.freq_subday_type,
            parameters.freq_subday_interval,
            parameters.freq_recurrence_factor,
            parameters.active_start_time,
        )

    if ssis_deployment.job.notification_email_address:
        try:
            db.agent_create_operator(ssis_deployment.job.notification_email_address)
        except SqlAgentOperatorException as ex:
            # TODO: log a warning properly, not just print the message
            print(ex)

        try:
            db.agent_create_notification(
                job_name, ssis_deployment.job.notification_email_address
            )
        except SqlAgentOperatorException as ex:
            # TODO: log a warning properly, not just print the message
            print(ex)
