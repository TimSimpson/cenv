# Cget-Env - Simple ToolChain / Environment Management

Cget-Env is a tool somewhat similar to PyEnv which lets you manage multiple Cget and CMake environments.

## Installation

Cget-Env works by installing imposter programs which look like CMake or Cget and live at the front of your path. When you call CMake, cenv can optionally pass a toolchain file every time.

To install, clone this repo, run the install script, then add `bin` to your path:

    git clone ${REPO_URL} cenv
    cd cenv

Then, in Linux:

    ./install-cenv.sh
    export PATH=$(pwd)/bin:"${PATH}"

in Windows:

    install-cenv
    set PATH=%CD%/bin;%PATH%


## Usage


    cenv toolchain list
        * default
    cenv toolchain add emscripten "${EMSCRIPTEN}/cmake/Modules/Platform/Emscripten.cmake"
    cenv toolchain add msvc-14.1 --from-template msvc-14.1

    cenv list
        - shows envs
    cenv create emscripten js
    cenv activate js

    cenv deactivate
        - turn off

Cget-Env requires Python 2 or 3.


## Storage

output/
    toolchains/
        emscripten.cenv.txt
        emscripten.cmake...
        msvc-15.0.cmake...
    envs/
        js  # <-- this is a cget directory

