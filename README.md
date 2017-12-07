[![Build Status](https://travis-ci.org/TimSimpson/cenv.svg?branch=master)](https://travis-ci.org/TimSimpson/cenv)

# Cget-Env - Simple ToolChain / Environment Management

Cget-Env is a tool somewhat similar to PyEnv and lets you manage multiple [Cget](https://github.com/pfultz2/cget) and [CMake](https://cmake.org/) environments.

It creates a directory called `~/.cenv` where it keeps track of unique instances of C++ packages which are managed by `cget` and can be used by `cmake`.

It also wraps `cmake` to force it to obey the environment variable `CGET_PREFIX` used by cget; every call you make to `cmake` will automatically add the arguments `-DCMAKE_TOOLCHAIN_FILE="${CGET_PREFIX}"/cget/cget.cmake` and `               -DCMAKE_INSTALL_PREFIX="${CGET_PREFIX}"`. This makes it easier to use CMake in conjunction with Cget and harder to inadvertently dirty your global packages.

## Usage

Check this out:

    $ cd some-project
    $ cenv list
    No envs found!
    $ cenv init typical-env
    Created new Env(name=typical-env, toolchain=None)
    $ cenv init clang-env --cxx clang++-3.8 --cc clang-3.8
    Created new Env(name=clang-env, toolchain=None)
    $ cenv set clang-env
    * * using clang-env
    $ mkdir build-clang && cd build-clang
    $ cmake -H../ -B./  # build using clang
    $ make install  # install libraries to ~/.cenv/envs/clang-env/lib
    $ cd ..
    $ cenv list
    * clang-env
      typical-env
    $ cenv init js --toolchain "${EMSCRIPTEN}/cmake/Modules/Platform/Emscripten.cmake"
    $ cenv set js
    * * using js
    $ cenv list
      clang-env
    * js
      typical-env
    $ cd ..
    $ mkdir build-js && cd build-js
    $ cmake -G Ninja -H../ -B./  $ build using Emscripten
    $ ninja install  # Installs stuff to ~/.cenv/envs/js/lib
    $ cenv set
    * * cenv deactivated

## Installation

Regardless of how you run cenv, you'll need the following:

* git
* cmake
* python

All of these must be available on your path. Additionally, `cget` is required but some of the methods mentioned below will install it.

### Windows Command Prompt

Git clone this repo, then run `install.bat` in your Command Prompt to get support for Cenv:

    > git clone https://github.com/TimSimpson/cenv.git
    > cd cenv
    > install.bat

You'll need to run `install.bat` each time you open up a prompt, or just add the lines the install script mentions to the batch file your Command Prompt always runs when it starts (if you're using a short cut to the Command Prompt that doesn't do this, you should really change your ways).

### Linux with Bash

First, clone and enter the repo:

    $ git clone https://github.com/TimSimpson/cenv.git
    $ cd cenv

If you're on Linux and using Python I recommend using [Pipsi](https://github.com/mitsuhiko/pipsi). If you have that installed, run this:

    $ pipsi install cget
    $ pipsi install -e ./

If you don't use Pipsi, but have an activate virtualenv, you can run:

    $ pip install cget
    $ pip install -e ./

If you don't know what any of this stuff is just run this:

    $ ./install.sh

Whatever you do, end by sourcing this file to enable Bash support:

    $ source resources/bash-support.sh
