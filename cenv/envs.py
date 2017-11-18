import os
import shutil
import subprocess

import typing as t  # NOQA
from . import toolchains  # NOQA
from . import types as ct  # NOQA
from . import views


Env = ct.Env
ToolChain = ct.ToolChain


class Manager(object):

    def __init__(self, root_env_dir, view=None):
        # type: (ct.FilePath, t.Optional[views.View]) -> None
        self._dir = root_env_dir  # type: ct.FilePath
        self._view = view or views.Silent()

    def create(self, name, toolchain):
        # type: (str, toolchains.ToolChain) -> Env
        prior = self.get(name)
        if prior is not None:
            raise ValueError('{} already exists at {}'.format(
                prior.name, prior.directory))
        new_env_directory = os.path.join(self._dir, name)
        os.mkdir(new_env_directory)
        cmd = [
            'cget',
            'init',
            '--prefix', new_env_directory,
            '--toolchain', toolchain.file_path
        ]
        self._view.run_command(' '.join(cmd))
        subprocess.check_call(cmd)
        return Env(name, ct.FilePath(new_env_directory))

    def delete(self, name):
        # type: (str) -> None
        env = self.get(name)
        if env is None:
            return
        if not env.directory.startswith(self._dir):
            # Avoid deleteing an environment we don't seem to own.
            raise RuntimeError("Environment in wrong place.")
        shutil.rmtree(env.directory)

    def get(self, name):
        # type: (str) -> t.Optional[Env]
        """Grabs a Env by name."""
        dir_path = os.path.join(self._dir, name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            return Env(name, ct.FilePath(dir_path))
        return None

    def list(self):
        # type: () -> t.List[Env]
        result = []  # type: t.List[Env]
        for file in os.listdir(self._dir):
            dir_path = os.path.join(self._dir, file)
            if os.path.isdir(dir_path):
                result.append(Env(file, ct.FilePath(dir_path)))

        return result

# def create()
# def switch(env):
#     # type: (ct.FilePath) -> None
#     """Switches to a different env."""
#     # change CGET_PREFIX path to env path
#     #
