EXEC catalog.set_object_parameter_value
     @object_type     = 20
   , @parameter_name  = $variable_name
   , @object_name     = $environment_name
   , @folder_name     = $folder_name
   , @project_name    = $project_name
   , @parameter_value = $variable_name
   , @value_type      = R
;
