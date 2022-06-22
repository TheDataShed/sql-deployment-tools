DECLARE @step_id           int
      , @on_success_action TINYINT
;

DECLARE cursor_job_steps CURSOR FOR
  SELECT step_id
       , CASE
           WHEN ROW_NUMBER() OVER (ORDER BY step_id DESC) = 1 THEN -- Last step
             1 -- Quit with success
          ELSE
            3  -- Go to next step
         END AS on_success_action
  FROM   msdb.dbo.sysjobsteps
  WHERE  EXISTS (
           SELECT *
           FROM   msdb.dbo.sysjobs
           WHERE  name = $job_name
           AND    job_id = sysjobsteps.job_id
         )
;

OPEN cursor_job_steps;

FETCH NEXT FROM cursor_job_steps INTO @step_id, @on_success_action;

WHILE @@FETCH_STATUS = 0
  BEGIN
    EXEC msdb.dbo.sp_update_jobstep
         @job_name          = $job_name
       , @step_id           = @step_id
       , @on_success_action = @on_success_action
    ;

    FETCH NEXT FROM cursor_job_steps INTO @step_id, @on_success_action;
  END
;

CLOSE cursor_job_steps;
DEALLOCATE cursor_job_steps;
