@ECHO OFF

if "%CENV_ROOT%"=="" (
    set CENV_ROOT=%HOME%\.cenv
)

%CENV_BIN_ROOT%\output\venv\Scripts\cenv.exe %*
if errorlevel 1 (
    exit /b %errorlevel%
) else (
    CALL "%CENV_ROOT%\set-vars.bat"
    exit /b %errorlevel%
)
