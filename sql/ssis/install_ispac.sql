DECLARE @project_binary varbinary(MAX)
      , @operation_id   bigint
;

/* Note: OPENROWSET cannot be parameterised, so we use token replacement instead. */
SET @project_binary = (SELECT * FROM OPENROWSET(BULK '{ispac_path}', SINGLE_BLOB) AS binary_data)

EXEC catalog.deploy_project
     @folder_name    = $folder_name
   , @project_name   = $project_name
   , @project_stream = @project_binary
   , @operation_id   = @operation_id OUT
;