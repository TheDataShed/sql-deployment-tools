DECLARE @schedule_id int;

EXEC msdb.dbo.sp_add_jobschedule
     @job_name               = $job_name
   , @name                   = $schedule_name
   , @enabled                = 1 -- Enabled
   , @freq_type              = $freq_type
   , @freq_interval          = $freq_interval
   , @freq_subday_type       = $freq_subday_type
   , @freq_subday_interval   = $freq_subday_interval
   , @freq_relative_interval = 0
   , @freq_recurrence_factor = $freq_recurrence_factor
   , @active_start_time      = $active_start_time
   , @schedule_id            = @schedule_id OUTPUT
;

EXEC msdb.dbo.sp_attach_schedule
     @job_name    = $job_name
   , @schedule_id = @schedule_id
;
