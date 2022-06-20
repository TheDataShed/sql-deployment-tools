DECLARE @step_id int;

DECLARE cursor_job_steps CURSOR FOR
  SELECT steps.step_id
  FROM   msdb.dbo.sysjobs AS jobs
   INNER
    JOIN msdb.dbo.sysjobsteps AS steps
      ON steps.job_id = jobs.job_id
  WHERE  jobs.name = $job_name
  ORDER
      BY steps.step_id DESC
;

OPEN cursor_job_steps;

FETCH NEXT FROM cursor_job_steps INTO @step_id;

WHILE @@FETCH_STATUS = 0
  BEGIN
    EXEC msdb.dbo.sp_delete_jobstep
         @job_name = $job_name
       , @step_id  = @step_id
    ;

    FETCH NEXT FROM cursor_job_steps INTO @step_id;
  END
;

CLOSE cursor_job_steps;
DEALLOCATE cursor_job_steps;
