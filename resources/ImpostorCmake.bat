@ECHO OFF


set args=%*
REM replace " with Q since quotes mess things up
set args=%args:"=Q%
REM remove "--build" from the args
set args_minus_build=%args:--build=%
if "%CGET_PREFIX%"=="" ( GOTO normal ) ELSE (
    REM if --build isn't in the text, don't inject.
    REM Yes, this is a horrible hack.
    IF "%args%"=="%args_minus_build%" (
        GOTO inject
    )
    GOTO normal
)

:normal
    echo CGET_PREFIX not set
    cmake %*
GOTO the_end

:inject
    cmake -DCMAKE_TOOLCHAIN_FILE=%CGET_PREFIX%\cget\cget.cmake -DCMAKE_INSTALL_PREFIX=%CGET_PREFIX% %*

GOTO the_end

:the_end
