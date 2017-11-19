@ECHO OFF

if "%CENV_ROOT%"=="" (
    set CENV_ROOT=%HOME%\.cenv
)

if "%CENV_BIN_ROOT%"=="" (
    set CENV_BIN_ROOT=%~dp0
)

%CENV_BIN_ROOT%\cenv.exe %*
if errorlevel 1 (
    exit /b %errorlevel%
) else (
    CALL "%CENV_ROOT%\set-vars.bat"
    exit /b %errorlevel%
)
