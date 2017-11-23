import os
import shutil
import subprocess

import typing as t  # NOQA
from . import types as ct  # NOQA
from . import views


CGET_PREFIX = os.environ.get('CGET_PREFIX', None)


class Env(object):

    def __init__(self, name, directory):
        # type: (str, ct.FilePath) -> None
        self._name = name
        self._directory = directory

    @property
    def active(self):
        # type: () -> bool
        if CGET_PREFIX is None or not CGET_PREFIX:
            return False
        return (os.path.abspath(self._directory).lower()
                == os.path.abspath(CGET_PREFIX).lower())

    def get_creation_info(self):
        # type: () -> str
        try:
            with open(os.path.join(self._directory, 'cenv-info.txt')) as f:
                return f.read()
        except BaseException:
            return "<info file not found>"

    @property
    def name(self):
        # type: () -> str
        return self._name

    @property
    def directory(self):
        # type: () -> ct.FilePath
        return self._directory

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, Env):
            return False
        return all((self._name == other._name,
                    self._directory == other._directory))

    def __repr__(self):
        # type: () -> str
        return "Env(name={}, directory={})".format(
            self._name, self._directory)


class Manager(object):

    def __init__(self, root_env_dir, view=None):
        # type: (ct.FilePath, t.Optional[views.View]) -> None
        self._dir = root_env_dir  # type: ct.FilePath
        self._view = view or views.Silent()

    def create(self, name, cget_args):
        # type: (str, t.List[str]) -> Env
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
        ] + cget_args
        self._view.run_command(' '.join(cmd))
        subprocess.check_call(cmd)
        with open(os.path.join(new_env_directory, "cenv-info.txt"), "w") as f:
            f.write(' '.join('"{}"'.format(arg) if ' ' in arg else arg
                             for arg in cget_args))
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
