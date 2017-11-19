@echo off

SET old_dir=%CD%
SET CENV_BIN_ROOT=%~dp0
cd %CENV_BIN_ROOT%

echo * * Building virtualenv for Python dependencies...

python --version
if errorlevel 1 (
    echo python not found. Aborting install!
    exit /b %errorlevel%
)
virtualenv output/wvenv
if errorlevel 1 (
    python -m venv output/wvenv
    if errorlevel 1 (
        echo Couldn't create Python virtualenv.
        exit /b %errorlevel%
    )
)
echo * * Installing CGet...
output\wvenv\Scripts\pip install cget
if errorlevel 1 (
    echo Couldn't install Cget.
    exit /b %errorlevel%
)
echo * * Installing Cenv...
output\wvenv\Scripts\pip install -e .\
if errorlevel 1 (
    echo Couldn't install Cenv.
    exit /b %errorlevel%
)

copy resources\ImpostorCmake.bat output\wvenv\Scripts\cmake.bat
copy resources\ImpostorCenv.bat output\wvenv\Scripts\cenv.bat

doskey cenv=CALL %CENV_BIN_ROOT%\output\wvenv\Scripts\cenv.bat $*
doskey cmake=%CENV_BIN_ROOT%\output\wvenv\Scripts\cmake.bat $*

echo * * CENV installed.
echo.
echo To make Cenv a permanent part of your command prompt, put the following
echo code in the Batch script that runs when your Command Prompt starts up:
echo.
echo doskey cenv=CALL %CENV_BIN_ROOT%\output\wvenv\Scripts\cenv.bat $*
echo doskey cmake=%CENV_BIN_ROOT%\output\wvenv\Scripts\cmake.bat $*

cd %old_dir%
