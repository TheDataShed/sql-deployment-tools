:: Install the required Python libraries, including `pyinstaller`
pip install ^
    --quiet ^
    --requirement requirements\build.txt

:: Keep things clean: destroy the `dist/windows/` directory if it exists.
rmdir /S /Q .\dist\windows

pyinstaller ^
    src/sql_deployment_tools.py ^
    --clean ^
    --noconfirm ^
    --log-level WARN ^
    --distpath="dist\windows" ^
    --onefile ^
    --console ^
    --add-data="src\sql\;sql"
    --paths="src" ^

:: Run the app to check it has at least built!
.\dist\windows\sql_deployment_tools --help
