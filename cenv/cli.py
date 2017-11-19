import os
import sys

import typing as t  # NOQA

from . import envs
from . import frontdoor
from . import options
from . import toolchains
from . import types as ct  # NOQA


cenv_registry = frontdoor.CommandRegistry("cenv")  # type: ignore
cmd = cenv_registry.decorate

tc_registry = frontdoor.CommandRegistry("toolchain")
tc_cmd = tc_registry.decorate


def get_options():
    # type: () -> options.Options
    root = os.path.expanduser(os.environ.get('CENV_ROOT', '~/.cenv'))
    return options.Options(ct.FilePath(root))


def get_env_manager():
    # type: () -> envs.Manager
    return envs.Manager(get_options().environments)


def get_toolchain_manager():
    # type: () -> toolchains.Manager
    return toolchains.Manager(get_options().toolchains)


@cmd('list', desc='List Cget envs')
def cmd_list(args):
    # type: (t.List[str]) -> int
    envs = get_env_manager().list()
    for env in envs:
        print('{} {}'.format('*' if env.active else ' ', env.name))
    else:
        print('No envs found!')
    return 0


@cmd('create', desc='Create a Cget env')
def cmd_create(args):
    # type: (t.List[str]) -> int
    if len(args) != 2:
        print('Usage: `create <toolchain> <new env name>')
        return 1

    toolchain_name = args[0]
    env_name = args[1]

    toolchain = get_toolchain_manager().get(toolchain_name)
    if toolchain is None:
        print('No such toolchain: {}'.format(toolchain_name))
        return 1

    env = get_env_manager().create(env_name, toolchain)

    print('Created new {}'.format(env))
    return 0


@cmd('toolchain', 'Work with toolchains')
def cmd_toolchain(args):
    # type: (t.List[str]) -> int
    return tc_registry.dispatch(args)


@tc_cmd('add', 'Create or import toolchain file')
def cmd_tc_add(args):
    # type: (t.List[str]) -> int
    if len(args) != 2:
        print('Usage: `add <name of toolchain> <path to toolchain cmake file>')
        return 1

    name = args[0]
    file_path = ct.FilePath(args[1])
    tc = get_toolchain_manager().add_from_file(name, file_path)
    print("Added new {}".format(tc))
    return 0


@tc_cmd('list', 'List toolchains')
def cmd_tc_list(args):
    # type: (t.List[str]) -> int
    tc_list = get_toolchain_manager().list()
    for tc in tc_list:
        print('{} {}'.format(' ', tc.name))
    else:
        print('No toolchains found!')
    return 0


def main():
    # type: () -> None
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(cenv_registry.dispatch(args))


if __name__ == "__main__":
    main()
