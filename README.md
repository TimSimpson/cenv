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

    cenv toolchain add emscripten "${EMSCRIPTEN}/cmake/Modules/Platform/Emscripten.cmake"
    cenv toolchain add msvc-14.1 --from-template msvc-14.1
    cenv toolchain list
      emscripten
    cenv toolchain add msvc-14.1 --from-template msvc-14.1
    cenv toolchain list
    cenv list
        - shows envs
    cenv create emscripten js
    cenv activate js

    cenv deactivate
        - turn off

Cget-Env requires Python 2 or 3.


## Installation

cenv can be installed the same as most Python projects.

TODO: Overview of how to do that.

Once you have `cmake`, `cget`, and `cenv` on the path, add the following to your bash.rc file or wherever you setup your shell:

    export CENV_ROOT="${CENV_ROOT:-$HOME/.cenv}"

    function cenv(){
        $(which cenv) "$@"
        if [ "${?}" -eq 0 ]; then
            source "${CENV_ROOT}"/cenv.rc
        fi
    }

    function cmake(){
        local cmake_path=$(which cmake)
        if [ "${CGET_PREFIX}" == "" ]; then
            $(which cmake) "${@}"
        else
            $(which cmake) \
                -DCMAKE_TOOLCHAIN_FILE="${CGET_PREFIX}"/cget/cget.cmake \
                -DCMAKE_INSTALL_PREFIX="${CGET_PREFIX}" \
                "${@}"
        fi
    }

These two functions wrap `cenv` and `cmake` respectively. `cenv` is wrapped to
allow a semi-portable Python script to set values in your shell, while `cmake`
is wrapped so always pass in the paths assocated with the currently selected
environment.

