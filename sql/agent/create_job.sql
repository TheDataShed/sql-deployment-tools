IF EXISTS (
  SELECT *
  FROM   msdb.dbo.sysjobs
  WHERE  name = $job_name
)
  BEGIN
    EXEC msdb.dbo.sp_update_job
         @job_name      = $job_name
       , @description   = $job_description
       , @start_step_id = 1
       , @enabled       = $job_enabled
    ;
  END
ELSE
  BEGIN
    EXEC msdb.dbo.sp_add_job
         @job_name              = $job_name
       , @description           = $job_description
       , @start_step_id         = 1
       , @enabled               = $job_enabled -- 1=Enabled
       , @notify_level_eventlog = 2 -- On failure
       , @notify_level_email    = 2 -- On failure
       , @notify_level_netsend  = 0 -- Never 
       , @notify_level_page     = 0 -- Never
       , @delete_level          = 0 -- Never
    ;

    EXEC msdb.dbo.sp_add_jobserver
         @job_name = $job_name
    ;
  END
;
