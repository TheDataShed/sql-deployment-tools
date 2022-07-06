import toml

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
            environment_name, folder_name, project_name, parameter.name, parameter.value
        )

    db.agent_create_job(job_name, job_description)

    for job_step in ssis_deployment.job.steps:

        if job_step._type != "SSIS":

            raise NotImplementedError(
                "Only job.steps.type==SSIS are currently supported"
            )

        db.agent_create_job_step_ssis(
            job_name,
            job_step.name,
            folder_name,
            project_name,
            job_step.package,
            environment_name,
            job_step.proxy,
        )

    for job_schedule in ssis_deployment.job.schedules:
        db.agent_create_job_schedule_occurs_every_n_minutes(
            job_name,
            job_schedule.name,
            job_schedule.every_n_minutes,
            job_schedule.start_time,
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
