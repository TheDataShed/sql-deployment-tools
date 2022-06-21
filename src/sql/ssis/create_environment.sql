IF NOT EXISTS (
  SELECT *
  FROM   SSISDB.internal.environments
   INNER
    JOIN SSISDB.internal.folders
      ON environments.folder_id = folders.folder_id
  WHERE  environments.environment_name = $environment_name
  AND    folders.name = $folder_name
)
  BEGIN
    EXEC SSISDB.catalog.create_environment
         @folder_name      = $folder_name
       , @environment_name = $environment_name
    ;
  END
;