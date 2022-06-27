DECLARE @environment_variable_name sysname;

DECLARE cursor_environment_variables CURSOR FOR
  SELECT environment_variables.name AS environment_variable_name
  FROM   SSISDB.internal.environments
   INNER
    JOIN SSISDB.internal.folders
      ON environments.folder_id = folders.folder_id
   INNER
    JOIN SSISDB.internal.environment_variables
      ON environment_variables.environment_id = environments.environment_id
  WHERE  environments.environment_name = $environment_name
  AND    folders.name = $folder_name
;

OPEN cursor_environment_variables;

FETCH NEXT FROM cursor_environment_variables INTO @environment_variable_name;

WHILE @@FETCH_STATUS = 0
  BEGIN
    EXEC SSISDB.catalog.delete_environment_variable
         @variable_name    = @environment_variable_name
       , @environment_name = $environment_name
       , @folder_name      = $folder_name
    ;

    FETCH NEXT FROM cursor_environment_variables INTO @environment_variable_name;
  END
;

CLOSE cursor_environment_variables;
DEALLOCATE cursor_environment_variables;
