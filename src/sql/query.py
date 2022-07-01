import pathlib


def get_sql(filename: str) -> str:
    """
    Utility method to read raw SQL from files in the ``sql/``
    subdirectory.

    :param filename: test data file
    :type filename: str
    :return: raw contents of a SQL file
    :rtype: str
    """
    with open(pathlib.Path(__file__).resolve().parent.joinpath(filename)) as i:
        return i.read()


ssis_create_folder = get_sql("sql/ssis/create_folder.sql")

ssis_create_environment = get_sql("sql/ssis/create_environment.sql")

ssis_create_environment_reference = get_sql("sql/ssis/create_environment_reference.sql")

ssis_remove_all_environment_variables = get_sql(
    "sql/ssis/remove_all_environment_variables.sql"
)

ssis_create_environment_variable = get_sql("sql/ssis/create_environment_variable.sql")

ssis_set_environment_variable_as_sensitive = get_sql(
    "sql/ssis/set_environment_variable_as_sensitive.sql"
)

agent_create_job = get_sql("sql/agent/create_job.sql")

agent_create_job_schedule = get_sql("sql/agent/create_job_schedule.sql")

agent_create_job_step = get_sql("sql/agent/create_job_step.sql")

agent_create_job_step_using_proxy = get_sql("sql/agent/create_job_step_using_proxy.sql")

agent_reset_job_step_flow = get_sql("sql/agent/reset_job_step_flow.sql")

agent_remove_all_alerts = get_sql("sql/agent/remove_all_alerts.sql")

agent_remove_all_schedules = get_sql("sql/agent/remove_all_schedules.sql")

agent_remove_all_steps = get_sql("sql/agent/remove_all_steps.sql")

agent_create_operator = get_sql("sql/agent/create_operator.sql")

agent_create_notification = get_sql("sql/agent/create_notification.sql")

ssis_install_ispac = get_sql("sql/ssis/install_ispac.sql")

ssis_set_environment_reference_to_variable = get_sql(
    "sql/ssis/set_environment_reference_to_variable.sql"
)

ssis_get_environment_reference_id = get_sql("sql/ssis/get_environment_reference_id.sql")
