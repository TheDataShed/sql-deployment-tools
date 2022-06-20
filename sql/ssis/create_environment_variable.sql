IF NOT EXISTS (
  SELECT  *
  FROM   SSISDB.internal.folders
   LEFT
    JOIN SSISDB.internal.environments
      ON folders.folder_id = environments.folder_id
   LEFT
    JOIN SSISDB.internal.environment_variables
      ON environments.environment_id = environment_variables.environment_id
   LEFT
    JOIN SSISDB.internal.projects
      ON projects.folder_id = folders.folder_id
  WHERE  folders.name = $folder_name
  AND    environments.environment_name = $environment_name
  AND    environment_variables.name = $variable_name
)
  BEGIN
    EXEC SSISDB.catalog.create_environment_variable
         @folder_name      = $folder_name
       , @environment_name = $environment_name
       , @variable_name    = $variable_name
       , @value            = $variable_value
       , @data_type        = N'String'
       , @sensitive        = false
    ;
  END
ELSE
  BEGIN
    EXEC SSISDB.catalog.set_environment_variable_value
         @folder_name      = $folder_name
       , @environment_name = $environment_name
       , @variable_name    = $variable_name
       , @value            = $variable_value
    ;
  END
;