@ECHO OFF

set args=%*
set args_minus_build=%args:--build=%

if "%CGET_PREFIX%"=="" ( GOTO normal ) ELSE (
    REM don't inject stuff as it messed up the --build command.
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
