EXEC SSISDB.catalog.set_environment_variable_protection
     @folder_name      = $folder_name
   , @environment_name = $environment_name
   , @variable_name    = $variable_name
   , @sensitive        = True
;