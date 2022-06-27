SELECT  reference_id AS environment_reference_id
FROM    catalog.environment_references
 INNER
  JOIN catalog.projects
    ON projects.project_id = environment_references.project_id
WHERE  environment_references.environment_name = $environment_name
AND    projects.name = $project_name
;
