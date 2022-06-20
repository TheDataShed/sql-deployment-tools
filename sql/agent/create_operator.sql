DECLARE @error_message varchar(500);

IF EXISTS (
  SELECT *
  FROM   msdb.dbo.sysoperators
  WHERE  enabled       = 1
  AND    name          = $operator_name
  AND    email_address = $email_address
)
  BEGIN
    PRINT 'Operator already exists, no work to do.';
  END
ELSE IF Coalesce(Is_SrvRoleMember(N'sysadmin'), 0) = 0
  BEGIN
    SET @error_message = 'Insufficient permissions to manage Operators (sysadmin required). Contact your DBA.';
  END
ELSE IF EXISTS (
     SELECT *
     FROM   msdb.dbo.sysoperators
     WHERE  name = $operator_name
   )
  BEGIN
    EXEC msdb.dbo.sp_update_operator
         @name          = $operator_name
       , @email_address = $email_address
    ;
  END
ELSE
  BEGIN
    EXEC msdb.dbo.sp_add_operator
         @name          = $operator_name
       , @email_address = $email_address
       , @enabled       = 1
    ;
  END
;

-- We must always return a result, otherwise PYODBC will throw an exception.
SELECT @error_message AS error_message;
