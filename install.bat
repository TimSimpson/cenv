@echo off

SET old_dir=%CD%
SET CENV_BIN_ROOT=%~dp0
cd %CENV_BIN_ROOT%

echo * * Building virtualenv for Python dependencies...

python -m venv output/venv
echo * * Installing CGet...
output\venv\Scripts\pip install cget
echo * * Installing Cenv...
output\venv\Scripts\pip install -e .\

cp resources\ImpostorCmake.bat output\venv\Scripts\cmake.bat
cp resources\ImpostorCenv.bat output\venv\Scripts\cenv.bat

doskey cenv=CALL %CENV_BIN_ROOT%\output\venv\Scripts\cenv.bat $*
doskey cmake=%CENV_BIN_ROOT%\output\venv\Scripts\cmake.bat $*

echo * * CENV installed.
echo.
echo To make Cenv a permanent part of your command prompt, put the following
echo code in the Batch script that runs when your Command Prompt starts up:
echo.
echo doskey cenv=CALL %CENV_BIN_ROOT%\output\venv\Scripts\cenv.bat $*
echo doskey cmake=%CENV_BIN_ROOT%\output\venv\Scripts\cmake.bat $*

cd %old_dir%
