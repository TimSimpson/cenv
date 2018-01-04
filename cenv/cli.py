from __future__ import print_function

import os
import sys
import textwrap

import typing as t  # NOQA

from . import envs
from . import frontdoor
from . import options
from . import path
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
    if len(args) < 1:
        print('Usage: `create <new env name> <cget --init args>')
        return 1

    env_name = args[0]

    extra_args = args[1:]

    if '--prefix' in extra_args or '-p' in extra_args:
        print('Invalid value `--prefix`: cenv sets this when calling cget.')
        return 1

    env = get_env_manager().create(env_name, extra_args)

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

    def write_file(script_type, file_path):
        # type: (str, str) -> None

        sep = {
            'bash': ':',
            'dos': ';',
        }[script_type]

        p = path.PathUpdater(sep)

        new_path_str = p.update_paths(
            'PATH',
            new_path=None if new_env is None else [new_env.bin, new_env.lib],
            old_path=None if old_env is None else [old_env.bin, old_env.lib])

        new_ld_library_path_str = p.update_paths(
            'LD_LIBRARY_PATH',
            new_path=None if new_env is None else new_env.lib,
            old_path=None if old_env is None else old_env.lib)

        template_args = {
            'cenv_name': '' if new_env is None else new_env.name,
            'cget_prefix': '' if new_env is None else new_env.directory,
            'path': new_path_str,
            'ld_library_path': new_ld_library_path_str,
        }

        comment = {
            'bash': '#',
            'dos': 'REM',
        }[script_type]
        export = {
            'bash': 'export',
            'dos': 'set',
        }[script_type]

        with open(file_path, 'w') as f:
            f.write(
                "{comment} This file was created by Cenv.\n"
                "{comment} It's intended to be used only once then deleted.\n"
                "{export} CENV_NAME={cenv_name}\n"
                "{export} CGET_PREFIX={cget_prefix}\n"
                "{export} PATH={path}\n"
                "{export} LD_LIBRARY_PATH={ld_library_path}\n"
                .format(comment=comment, export=export, **template_args))

    ops = get_options()
    write_file('bash', ops.rc_file)
    write_file('dos', ops.batch_file)

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
