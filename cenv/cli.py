from __future__ import print_function

import argparse
import os
import sys
import textwrap

import typing as t  # NOQA

from . import envs
from . import frontdoor
from . import options
from . import scripts
from . import types as ct  # NOQA


cenv_registry = frontdoor.CommandRegistry("cenv")  # type: ignore
cmd = cenv_registry.decorate


def get_options():
    # type: () -> options.Options
    default_root = os.path.join('~', '.cenv')
    root = os.path.expanduser(os.environ.get('CENV_ROOT', default_root))
    ops = options.Options(ct.FilePath(root))
    if not os.path.exists(ops.environments):
        os.makedirs(ops.environments)
    return ops


def get_env_manager():
    # type: () -> envs.Manager
    return envs.Manager(get_options().environments)


@cmd(['l', 'list'], desc='List Cget envs (use -v for verbose mode)')
def cmd_list(args):
    # type: (t.List[str]) -> int
    verbose_mode = '-v' in args or '--verbose' in args
    envs = get_env_manager().list()
    if len(envs) == 0:
        print("No envs found!")
    else:
        envs.sort(key=lambda env: env.name if env.managed else '')
        for env in envs:
            active = '*' if env.active else ' '
            if verbose_mode:
                print('{} {}\t{}'.format(
                    active, env.name, env.get_creation_info()))
            else:
                print('{} {}'.format(active, env.name))
            if not env.managed:
                print('    ^- full path: {}'.format(env.directory))

    return 0


@cmd('init', desc='Create a Cget env')
def cmd_init(args):
    # type: (t.List[str]) -> int
    cget_init_with = '--cget-init'

    parser = argparse.ArgumentParser(description="creates a new cenv")
    parser.add_argument("name",
                        type=str,
                        help="Name of cenv")
    parser.add_argument(cget_init_with,
                        nargs="+",
                        help='args passed to `cget --init`',
                        default=[],
                        required=False)
    parser.add_argument('--conan-profile',
                        type=str,
                        help='args passed to `cget --init`',
                        default=None)

    if len(args) < 1:
        print('Usage: `init <new env name> <cget --init args>')
        return 1

    if cget_init_with in args:
        cget_index = args.index(cget_init_with)
        cget_args = args[cget_index + 1:]
        other_args = args[0:cget_index]
    else:
        cget_args = []
        other_args = args

    p_args = parser.parse_args(other_args)

    if '--prefix' in cget_args or '-p' in cget_args:
        print('Invalid value `--prefix`: cenv sets this when calling cget.')
        return 1

    env = get_env_manager().create(p_args.name, cget_args)

    print('Created new {}'.format(env))
    return 0


def _set_env(managed, env_name):
    # type: (bool, t.Optional[str]) -> int

    env_manager = get_env_manager()

    old_env = env_manager.find_active_env()

    if env_name is not None:
        new_env = env_manager.get(managed, env_name)
        if new_env is None:
            if managed:
                print("No such environment {}".format(env_name))
            else:
                print('"{0}" is not a directory or does not contain a valid '
                      'toolchain file at "{0}/cget/cget.cmake".'
                      .format(env_name))
            return 1
    else:
        new_env = None

    ops = get_options()
    scripts.write_file(old_env, new_env, 'bash', ops.rc_file)
    scripts.write_file(old_env, new_env, 'dos', ops.batch_file)

    if new_env:
        print('* * using {}'.format(new_env.name))
    else:
        print('* * cenv deactivated')
    return 0


@cmd(['s', 'set'], desc='Sets current Cget env', help=textwrap.dedent("""
        Usage:

            cenv set <name>

        Finds an environment given by argument <name> and activates it,
        setting CGET_PREFIX to it's directory and CENV_NAME to <name>. Calls
        to CMake without the argument `--build` will pass the toolchain
        located in the environments directory at `./cget/cget.cmake`.

        To activate an environment created by cget directly, pass the
        argument `--dir` followed by a directory path, like so:

            cenv set --dir <directory-path>

        CENV_NAME will be set to the last component of the directory path
        (unless it is `cget`) with the prefix "dir:".

     """))
def cmd_set(args):
    # type: (t.List[str]) -> int
    if len(args) == 0:
        return _set_env(False, None)
    elif len(args) == 1:
        return _set_env(True, args[0])
    elif len(args) == 2:
        if args[0] == '--dir':
            return _set_env(False, args[1])
        else:
            print('Expected an option ("--dir") as argument 1, got {}.'
                  .format(args[0]))
            return 1
    else:
        print('Usage: cenv set [cenv-name]')
        return 1


@cmd('deactivate', desc='Turn off cenvs (cmake and cget behave normally)')
def cmd_deactive(args):
    # type: (t.List[str]) -> int
    return _set_env(False, None)


def main():
    # type: () -> None
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(cenv_registry.dispatch(args))


if __name__ == "__main__":  # pragma: nocover
    main()
