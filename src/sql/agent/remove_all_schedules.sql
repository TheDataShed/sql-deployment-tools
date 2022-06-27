DECLARE @schedule_id int;

DECLARE cursor_job_schedule CURSOR FOR
  SELECT schedules.schedule_id
  FROM   msdb.dbo.sysjobs AS jobs
   INNER
    JOIN msdb.dbo.sysjobschedules AS schedules
      ON schedules.job_id = jobs.job_id
  WHERE  jobs.name = $job_name
;

OPEN cursor_job_schedule;

FETCH NEXT FROM cursor_job_schedule INTO @schedule_id;

WHILE @@FETCH_STATUS = 0
  BEGIN
    EXEC msdb.dbo.sp_detach_schedule
         @job_name               = $job_name
       , @schedule_id            = @schedule_id
       , @delete_unused_schedule = 1
    ;

    FETCH NEXT FROM cursor_job_schedule INTO @schedule_id;
  END
;

CLOSE cursor_job_schedule;
DEALLOCATE cursor_job_schedule;
