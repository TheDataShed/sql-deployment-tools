IF NOT EXISTS (SELECT * FROM internal.folders WHERE name = $folder_name)
  BEGIN
    EXEC SSISDB.catalog.create_folder
        @folder_name = $folder_name
    ;
  END
;
