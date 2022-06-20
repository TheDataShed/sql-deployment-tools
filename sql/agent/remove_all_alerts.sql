DECLARE @alert_name sysname;

DECLARE cursor_alert CURSOR FOR
  SELECT alerts.name
  FROM   msdb.dbo.sysjobs AS jobs
   INNER
    JOIN msdb.dbo.sysalerts AS alerts
      ON alerts.job_id = jobs.job_id
  WHERE  jobs.name = $job_name
;

OPEN cursor_alert;

FETCH NEXT FROM cursor_alert INTO @alert_name;

WHILE @@FETCH_STATUS = 0
  BEGIN
    EXEC msdb.dbo.sp_delete_alert
         @name = @alert_name
    ;

    FETCH NEXT FROM cursor_alert INTO @alert_name;
  END
;

CLOSE cursor_alert;
DEALLOCATE cursor_alert;
