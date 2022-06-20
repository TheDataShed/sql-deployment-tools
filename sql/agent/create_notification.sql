DECLARE @error_message varchar(500);

IF EXISTS (
     SELECT *
     FROM   msdb.dbo.sysoperators
     WHERE  name = $operator_name
   )
  BEGIN
    EXEC msdb.dbo.sp_update_job
        @job_name                   = $job_name
      , @notify_email_operator_name = $operator_name
      , @notify_level_email         = $notify_level_email
    ;
  END
ELSE
  BEGIN
    SET @error_message = 'Operator does not exist. This is likely due to previous errors/warnings.';
  END
;

-- We must always return a result, otherwise PYODBC will throw an exception.
SELECT @error_message AS error_message;
