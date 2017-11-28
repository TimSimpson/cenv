@ECHO OFF


set args=%*
if [%args%] == [] goto normal
if "%CGET_PREFIX%"=="" goto normal

REM replace " with 'ESCAPE_QUOTE_HACK' since quotes mess things below up
set args=%args:"=ESCAPE_QUOTE_HACK%

REM remove "--build" from the args to from the variable `args_minus_build`
set args_minus_build=%args:--build=%

REM if `--build` isn't in the text, don't inject.
REM Yes, I know this is a horrible hack and I feel terrible about it.
IF "%args%"=="%args_minus_build%" (
    GOTO inject
) else (
    GOTO normal
)

:normal
    cmake %*
GOTO the_end

:inject
    cmake -DCMAKE_TOOLCHAIN_FILE=%CGET_PREFIX%\cget\cget.cmake -DCMAKE_INSTALL_PREFIX=%CGET_PREFIX% %*

GOTO the_end

:the_end
