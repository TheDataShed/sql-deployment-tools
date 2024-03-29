DECLARE @schedule_id int;

EXEC msdb.dbo.sp_add_jobschedule
     @job_name               = $job_name
   , @name                   = $schedule_name
   , @enabled                = 1 -- Enabled
   , @freq_type              = 4 -- Daily
   , @freq_interval          = 1 -- Once
   , @freq_subday_type       = 4 -- Every N Minutes
   , @freq_subday_interval   = $occurs_every_n_minutes
   , @freq_relative_interval = 0
   , @freq_recurrence_factor = 1
   , @active_start_time      = $hh_mm_ss
   , @schedule_id            = @schedule_id OUTPUT
;

EXEC msdb.dbo.sp_attach_schedule
     @job_name    = $job_name
   , @schedule_id = @schedule_id
;
