SELECT reference_id AS environment_reference_id
FROM   SSISDB.catalog.environment_references
 INNER
  JOIN SSISDB.catalog.projects
    ON projects.project_id = environment_references.project_id
 INNER
  JOIN SSISDB.catalog.folders
    ON folders.folder_id = projects.folder_id
WHERE  environment_references.environment_name = $environment_name
AND    projects.name = $project_name
AND    folders.name = $folder_name
;
