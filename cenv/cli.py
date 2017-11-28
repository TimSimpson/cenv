import os
import sys

import typing as t  # NOQA

from . import envs
from . import frontdoor
from . import options
from . import path
from . import types as ct  # NOQA


cenv_registry = frontdoor.CommandRegistry("cenv")  # type: ignore
cmd = cenv_registry.decorate


def output(text):
    # type: (str) -> None
    """Exactly like print, but easier to monkeypatch.

    I don't like the fixtures that capture stdout.
    """
    print(text)


def get_options():
    # type: () -> options.Options
    default_root = os.path.join('~', '.cenv')
    root = os.path.expanduser(os.environ.get('CENV_ROOT', default_root))
    ops = options.Options(ct.FilePath(root))
    if not os.path.exists(ops.environments):
        os.makedirs(ops.environments)
    if not os.path.exists(ops.toolchains):
        os.makedirs(ops.toolchains)
    return ops


def get_env_manager():
    # type: () -> envs.Manager
    return envs.Manager(get_options().environments)


@cmd('list', desc='List Cget envs (use -v for verbose mode)')
def cmd_list(args):
    # type: (t.List[str]) -> int
    verbose_mode = '-v' in args or '--verbose' in args
    envs = get_env_manager().list()
    if len(envs) == 0:
        output("No envs found!")
    else:
        for env in envs:
            active = '*' if env.active else ' '
            if verbose_mode:
                output('{} {}\t{}'.format(
                    active, env.name, env.get_creation_info()))
            else:
                output('{} {}'.format(active, env.name))

    return 0


@cmd('create', desc='Create a Cget env')
def cmd_create(args):
    # type: (t.List[str]) -> int
    if len(args) < 1:
        output('Usage: `create <new env name> <cget --init args>')
        return 1

    env_name = args[0]

    extra_args = args[1:]

    if '--prefix' in extra_args or '-p' in extra_args:
        output('Invalid value `--prefix`: cenv sets this when calling cget.')
        return 1

    env = get_env_manager().create(env_name, extra_args)

    output('Created new {}'.format(env))
    return 0


@cmd('activate', desc='Turn on Cget env')
def cmd_activate(args):
    # type: (t.List[str]) -> int
    if len(args) != 1:
        output('Usage: `activate <env name>')
        return 1

    env_name = args[0]

    env_manager = get_env_manager()

    old_env = env_manager.find_active_env()
    new_env = env_manager.get(env_name)

    if new_env is None:
        output("No such environment {}".format(env_name))
        return 1

    old_paths = path.get_paths()
    new_paths = path.update_paths(
        old_paths,
        new_path=new_env.lib,
        old_path=None if old_env is None else old_env.lib)
    new_path_str = path.set_paths(new_paths)

    ops = get_options()
    with open(ops.rc_file, 'w') as f:
        f.write("# This file was created by Cenv.\n"
                "# It's intended to be used only once then deleted.\n"
                "export CGET_PREFIX={cget_prefix}\n"
                "export PATH={path}\n".format(
                        cget_prefix=new_env.directory,
                        path=new_path_str
                    ))
    with open(ops.batch_file, 'w') as f:
        f.write("REM This file was created by Cenv.\n"
                "REM It's intended to be used only once then deleted.\n"
                "set CGET_PREFIX={cget_prefix}\n"
                "set PATH={path}\n".format(
                        cget_prefix=new_env.directory,
                        path=new_path_str
                    ))

    return 0


@cmd('deactivate', desc='Turn off cenvs (cmake and cget behave normally)')
def cmd_deactive(args):
    # type: (t.List[str]) -> int
    ops = get_options()
    with open(ops.rc_file, 'w') as f:
        f.write("export CGET_PREFIX=")
    with open(ops.batch_file, 'w') as f:
        f.write("set CGET_PREFIX=")
    return 0


def main():
    # type: () -> None
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(cenv_registry.dispatch(args))


if __name__ == "__main__":
    main()
