[![Build Status](https://travis-ci.org/TimSimpson/cenv.svg?branch=master)](https://travis-ci.org/TimSimpson/cenv)

# Cenv - Simple C Environment Management

Cenv is a tool somewhat similar to PyEnv and lets you manage multiple "c-environments" (or "cenvs" for short). It works by managing a collection of "c envs" (also known as "prefix paths", or "installation paths") and making it easy to work with them by swapping around environment variables for you. 

In particular, it does the following:

* Automatically updates `PATH` and `LD_LIBRARY_PATH` to include the `bin` and `lib` directories in a given cenv, and unsets them when you're done.
* Works with the awesome [Cget](https://github.com/pfultz2/cget) by setting the `CGET_PREFIX` var so `cget install` installs dependencies to the right spot.
* Provides a shell specific wrapper for [CMake](https://cmake.org/) so that `-DCMAKE_TOOLCHAIN_FILE` is automatically passed the `cget` toolchain, and `-DCMAKE_INSTALL_PREFIX` gets the cenv path (CMake has _finally_ added the ability to read defaults for these settings from environment variables but as of 2025 the latest LTS of Ubuntu still gives me the version that won't work and instead dirties the system by default, so I'm keeping this in for now)

# TODO

[ ] Set DCMAKE_INSTALL_PREFIX when switching environments
[ ] Set DCMAKE_TOOLCHAIN_FILE if the toolchain file is there
[ ] Allow creating a new cenv without using cget since we live in the worst timeline
[ ] Potentially explain race condition?

## Usage

Check this out:

    $ cd some-project
    $ cenv list
    No envs found!
    $ cenv init typical-env
    Created new Env(name=typical-env, toolchain=None)
    $ cenv init clang-env --cxx clang++-3.8 --cc clang-3.8
    Created new Env(name=clang-env, toolchain=None)
    $ cenv set clang-env  # Note: by default this tool doesn't change your prompt. This is for illustration.
    * * using clang-env
    {clang-env} $ mkdir build-clang && cd build-clang
    {clang-env} $ cmake -H../ -B./  # build using clang
    {clang-env} $ make install  # installs binaries to ~/.cenv/envs/clang-env
    {clang-env} $ my-app  # runs ~/.cenv/envs/clang-env/bin/my-app
    {clang-env} $ cd ..
    {clang-env} $ cenv list
    * clang-env
      typical-env
    {clang-env} $ cenv init js --toolchain "${EMSCRIPTEN}/cmake/Modules/Platform/Emscripten.cmake"
    {clang-env} $ cenv set js
    * * using js
    {js} $ cenv list
      clang-env
    * js
      typical-env
    {js} $ cd ..
    {js} $ mkdir build-js && cd build-js
    {js} $ cmake -G Ninja -H../ -B./  # builds using Emscripten
    {js} $ ninja install  # Installs stuff to ~/.cenv/envs/js/lib
    {js} $ cenv set
    * * cenv deactivated
    $

## Features:

### Shell Integration via Bash and Batch Files

This project contains integrates with the Windows Command Prompt and Bash shells to manipulate environment variables when you switch cenvs.

This means you can easily run binaries with dynamic libs as the libaries, installed to the cenv, will be on your path.

The integration also wraps cmake itself with an alias or a doskey macro which automatically passes the tool chain file created by cget as an argument (except when `--build` is passed). Though controversial it makes switching to a new cenv painless.

Important note: the environment variable `CMAKE_PREFIX_PATH` can also cause all invocations of CMake to set the prefix path- but there's no way to force CMake to automatically use a toolchain. Unless you're a huge fan of obtuse linker errors caused by combining libraries built with different settings, it's best to always use the same toolchain and configuration for all the binaries installed to a cenv. This means its necessary to always pass the toolchain produced by cget (which also sets the prefix path and makes using the `CMAKE_PREFIX_PATH` environment variable unnecessary).

It also sets the environment variable `CENV_NAME`, which you can display in your prompt if you so wish.

### Central location for c-environments.

By default, cget creates a cenv in a directory `./cget`, which is great for CI or other cases where you want to create an entire cenv to be used exclusively by one project or working directory. However sometimes it can be preferrable to keep a number of cenvs in a central location where they can be easily accessed and reused from your current shell.

This tool creates a directory called `~/.cenv/envs` where it stores multiple c-environments.

If you'd like to use the shell integration features for directories outside of this location, you can do that like so:

    $ mkdir build && cd build
    $ cenv set ./my-project/cget
    {my-project} $


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
