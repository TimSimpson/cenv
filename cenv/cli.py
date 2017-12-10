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


@cmd(['l', 'list'], desc='List Cget envs (use -v for verbose mode)')
def cmd_list(args):
    # type: (t.List[str]) -> int
    verbose_mode = '-v' in args or '--verbose' in args
    envs = get_env_manager().list()
    if len(envs) == 0:
        output("No envs found!")
    else:
        envs.sort(key=lambda env: env.name)
        for env in envs:
            active = '*' if env.active else ' '
            if verbose_mode:
                output('{} {}\t{}'.format(
                    active, env.name, env.get_creation_info()))
            else:
                output('{} {}'.format(active, env.name))

    return 0


@cmd('init', desc='Create a Cget env')
def cmd_init(args):
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

    return _set_env(args[0])


def _set_env(env_name):
    # type: (t.Optional[str]) -> int

    env_manager = get_env_manager()

    old_env = env_manager.find_active_env()

    if env_name is not None:
        new_env = env_manager.get(env_name)
        if new_env is None:
            output("No such environment {}".format(env_name))
            return 1
    else:
        new_env = None

    new_path_str = path.update_paths(
        'PATH',
        new_path=None if new_env is None else new_env.lib,
        old_path=None if old_env is None else old_env.lib)

    new_ld_library_path_str = path.update_paths(
        'LD_LIBRARY_PATH',
        new_path=None if new_env is None else new_env.lib,
        old_path=None if old_env is None else old_env.lib)

    template_args = {
        'cenv_name': '' if new_env is None else new_env.name,
        'cget_prefix': '' if new_env is None else new_env.directory,
        'path': new_path_str,
        'ld_library_path': new_ld_library_path_str,
    }
    ops = get_options()
    with open(ops.rc_file, 'w') as f:
        f.write("# This file was created by Cenv.\n"
                "# It's intended to be used only once then deleted.\n"
                "export CENV_NAME={cenv_name}\n"
                "export CGET_PREFIX={cget_prefix}\n"
                "export PATH={path}\n"
                "export LD_LIBRARY_PATH={ld_library_path}\n"
                .format(**template_args))
    with open(ops.batch_file, 'w') as f:
        f.write("REM This file was created by Cenv.\n"
                "REM It's intended to be used only once then deleted.\n"
                "set CENV_NAME={cenv_name}\n"
                "set CGET_PREFIX={cget_prefix}\n"
                "set PATH={path}\n"
                "set LD_LIBRARY_PATH={ld_library_path}\n"
                .format(**template_args))

    if new_env:
        print('* * using {}'.format(new_env.name))
    else:
        print('* * cenv deactivated')
    return 0


@cmd(['s', 'set'], desc='Sets current Cget env')
def cmd_set(args):
    # type: (t.List[str]) -> int
    if len(args) == 0:
        return _set_env(None)
    elif len(args) == 1:
        return _set_env(args[0])
    else:
        print('Usage: cenv set [cenv-name]')
        return 1


@cmd('deactivate', desc='Turn off cenvs (cmake and cget behave normally)')
def cmd_deactive(args):
    # type: (t.List[str]) -> int
    return _set_env(None)


def main():
    # type: () -> None
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(cenv_registry.dispatch(args))


if __name__ == "__main__":
    main()
