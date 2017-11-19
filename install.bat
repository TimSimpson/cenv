SET old_dir=%CD%
SET CENV_BIN_ROOT=%~dp0
cd %CENV_BIN_ROOT%
python -m venv output/venv
output\venv\Scripts\pip install cget
output\venv\Scripts\pip install -e .\

cp resources\ImpostorCmake.bat output\venv\Scripts\cmake.bat

doskey cenv=CALL %CENV_BIN_ROOT%\output\venv\Scripts\cenv.exe $*
doskey cmake=%CENV_BIN_ROOT%\output\venv\Scripts\cmake.bat $*
