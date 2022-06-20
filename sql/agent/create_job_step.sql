EXEC msdb.dbo.sp_add_jobstep
     @job_name             = $job_name
   , @step_name            = $step_name
   , @cmdexec_success_code = 0
   , @on_success_action    = 1 -- Quit with success
   , @on_fail_action       = 2 -- Quit with failure
   , @subsystem            = $sub_system
   , @command              = $command
   , @database_name        = $database_name
;