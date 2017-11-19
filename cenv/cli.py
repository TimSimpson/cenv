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


@cmd('list', desc='List Cget envs (use -v for verbose mode)')
def cmd_list(args):
    # type: (t.List[str]) -> int
    verbose_mode = '-v' in args or '--verbose' in args
    envs = get_env_manager().list()
    if len(envs) == 0:
        print("No envs found!")
    else:
        for env in envs:
            active = '*' if env.active else ' '
            if verbose_mode:
                print('{} {}\t{}'.format(
                    active, env.name, env.get_creation_info()))
            else:
                print('{} {}'.format(active, env.name))

    return 0


@cmd('create', desc='Create a Cget env')
def cmd_create(args):
    # type: (t.List[str]) -> int
    if len(args) < 1:
        print('Usage: `create <toolchain> <new env name>')
        return 1

    env_name = args[0]

    extra_args = args[1:]

    if '--prefix' in extra_args or '-p' in extra_args:
        print('Invalid value `--prefix`: cenv sets this when calling cget.')
        return 1

    toolchain_arg = None  # type: t.Optional[t.Dict[str, t.Any]]
    for i, arg in enumerate(extra_args):
        if "--toolchain" == arg:
            if i < len(extra_args) - 1:
                toolchain_arg = {
                    'index': i + 1, 'name': extra_args[i + 1], 'embed': True
                }
                break
            else:
                print('Expected name after `--toolchain`.')
                return 1
        elif arg.startswith("--toolchain="):
            toolchain_arg = {
                'index': i, 'name': extra_args[i][12:], 'embed': True
            }
            break

    if toolchain_arg is not None:
        toolchain = get_toolchain_manager().get(toolchain_arg['name'])
        if toolchain is None:
            if not os.path.exists(toolchain_arg['name']):
                print('Warning: No such toolchain: {}'.format(
                    toolchain_arg['name']))
                print('Env may be inoperable.')
        else:
            # Mutate the arg headed to cget
            if toolchain_arg['embed']:
                extra_args[toolchain_arg['index']] = '--toolchain={}'.format(
                    toolchain.file_path)
            else:
                extra_args[toolchain_arg['index']] = toolchain.file_path

    env = get_env_manager().create(env_name, extra_args)

    print('Created new {}'.format(env))
    return 0


@cmd('activate', desc='Turn on Cget env')
def cmd_activate(args):
    # type: (t.List[str]) -> int
    if len(args) != 1:
        print('Usage: `activate <env name>')
        return 1

    env_name = args[0]

    env = get_env_manager().get(env_name)

    if env is None:
        print("No such environment {}".format(env_name))
        return 1

    ops = get_options()
    with open(ops.rc_file, 'w') as f:
        f.write("export CGET_PREFIX={}".format(env.directory))

    return 0


@cmd('deactivate', desc='Turn off cenvs (cmake and cget behave normally)')
def cmd_deactive(args):
    # type: (t.List[str]) -> int
    ops = get_options()
    with open(ops.rc_file, 'w') as f:
        f.write("export CGET_PREFIX=")
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
    if len(tc_list) == 0:
        print('No toolchains found!')
    else:
        for tc in tc_list:
            print('{} {}'.format(' ', tc.name))
    return 0


def main():
    # type: () -> None
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(cenv_registry.dispatch(args))


if __name__ == "__main__":
    main()
