import os
import sys

import typing as t  # NOQA

from . import envs
from . import frontdoor
from . import options
from . import toolchains
from . import types as ct  # NOQA


REGISTRY = frontdoor.CommandRegistry("cenv")  # type: ignore
cmd = REGISTRY.decorate


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


@cmd('list')
def cmd_list(args):
    # type: (t.List[str]) -> int
    envs = get_env_manager().list()
    for env in envs:
        print('{} {}'.format(' ', env.name))
    return 0


def main():
    # type: () -> None
    # Fix goofy bug when using Windows command prompt to ssh into Vagrant box
    # that puts \r into the strings.
    args = [arg.strip() for arg in sys.argv[1:]]
    sys.exit(REGISTRY.dispatch(args))


if __name__ == "__main__":
    main()
