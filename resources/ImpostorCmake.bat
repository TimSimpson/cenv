@ECHO OFF

if "%CGET_PREFIX%"=="" GOTO normal ELSE inject

:normal
    echo CGET_PREFIX not set
    cmake %*
GOTO the_end

:inject
    cmake -DCMAKE_TOOLCHAIN_FILE=%CGET_PREFIX%\cget\cget.cmake -DCMAKE_INSTALL_PREFIX=%CGET_PREFIX% %*

GOTO the_end

:the_end
