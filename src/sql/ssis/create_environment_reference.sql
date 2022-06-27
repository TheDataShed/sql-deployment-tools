DECLARE @reference_id bigint;

IF NOT EXISTS (
  SELECT *
  FROM   SSISDB.internal.environment_references
   INNER
    JOIN SSISDB.internal.projects
      ON projects.project_id = environment_references.project_id
   INNER
    JOIN SSISDB.internal.folders
      ON folders.folder_id = projects.folder_id
  WHERE  environment_references.environment_name = $environment_name
  AND    projects.name = $project_name
  AND    folders.name = $folder_name
)
  BEGIN
    EXEC SSISDB.catalog.create_environment_reference
         @environment_name = $environment_name
       , @project_name     = $project_name
       , @folder_name      = $folder_name
       , @reference_type   = R
       , @reference_id     = @reference_id OUTPUT
    ;
  END
;
