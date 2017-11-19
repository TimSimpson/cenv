# Cget-Env - Simple ToolChain / Environment Management

Cget-Env is a tool somewhat similar to PyEnv which lets you manage multiple Cget and CMake environments.

## Usage

Check this out:

    $ cd some-project
    $ cenv list
    No envs found!
    $ cenv create typical-env
    Created new Env(name=typical-env, toolchain=None)
    $ cenv create clang-env --cxx clang++-3.8 --cc clang-3.8
    Created new Env(name=clang-env, toolchain=None)
    $ cenv activate clang-env
    $ mkdir build-clang && cd build-clang
    $ cmake -H../ -B./  # build using clang
    $ make install  # install libraries to ~/.cenv/envs/clang-env/lib
    $ cd ..
    $ cenv list
    * clang-env
      typical-env
    $ cenv toolchain add emscripten "${EMSCRIPTEN}/cmake/Modules/Platform/Emscripten.cmake"
    $ cenv toolchain list
      emscripten
    $ cenv create js --toolchain emscripten
    $ cenv activate js
    $ cenv list
      clang-env
    * js
      typical-env
    $ cd ..
    $ mkdir build-js && cd build-js
    $ cmake -G Ninja -H../ -B./  $ build using Emscripten
    $ ninja install  # Installs stuff to ~/.cenv/envs/js/lib
    $ cenv deactivate


## Installation

`cenv` (this project) can be installed the same as most Python projects.

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
