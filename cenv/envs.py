import json
import os
import shutil
import subprocess

import typing as t  # NOQA
from . import types as ct  # NOQA
from . import views


CGET_PREFIX = os.environ.get('CGET_PREFIX', None)


class Env(object):

    def __init__(self, name, directory, managed=True):
        # type: (str, ct.FilePath, bool) -> None
        self._name = name
        self._directory = directory
        self._managed = managed

        self.__details = None  # type: t.Optional[dict]

    @property
    def active(self):
        # type: () -> bool
        if CGET_PREFIX is None or not CGET_PREFIX:
            return False
        return (os.path.abspath(self._directory).lower()
                == os.path.abspath(CGET_PREFIX).lower())

    @property
    def bin(self):
        # type: () -> str
        return os.path.join(self._directory, 'bin')

    @property
    def conan_profile(self):
        # type: () -> t.Optional[str]
        return self._details.get('conan_profile')

    @property
    def _details(self):
        # type: () -> dict
        if self.__details is None:
            try:
                with open(os.path.join(self._directory, 'cenv-info.txt')) as f:
                    self.__details = json.loads(f.read())
            except BaseException:
                self.__details = {}
        return self.__details

    def get_creation_info(self):
        # type: () -> str
        if 'cget_init_args' in self._details:
            return ' '.join(self._details.get('cget_init_args', []))
        else:
            return "<info file not found>"

    @property
    def managed(self):
        # type: () -> bool
        return self._managed

    @property
    def name(self):
        # type: () -> str
        return self._name

    @property
    def directory(self):
        # type: () -> ct.FilePath
        return self._directory

    @property
    def lib(self):
        # type: () -> str
        return os.path.join(self._directory, 'lib')

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

    def create(self, name, cget_init_args, conan_profile):
        # type: (str, t.List[str], t.Optional[str]) -> Env

        prior = self.get(True, name)
        if prior is not None:
            raise ValueError('{} already exists at {}'.format(
                prior.name, prior.directory))
        new_env_directory = os.path.join(self._dir, name)
        os.mkdir(new_env_directory)
        cmd = [
            'cget',
            'init',
            '--prefix', new_env_directory,
        ] + cget_init_args
        self._view.run_command(' '.join(cmd))
        subprocess.check_call(cmd)
        with open(os.path.join(new_env_directory, "cenv-info.txt"), "w") as f:
            f.write(json.dumps(
                {
                    "cget_init_args": cget_init_args,
                    "conan_profile": conan_profile,
                },
                indent=4))
        return Env(name, ct.FilePath(new_env_directory))

    def delete(self, name):
        # type: (str) -> None
        env = self.get(True, name)
        if env is None:
            return
        if not self._manages_directory(env.directory):
            # Avoid deleteing an environment we don't seem to own.
            raise RuntimeError("It doesn't look like cenv manages this "
                               "environment.")
        shutil.rmtree(env.directory)

    def _manages_directory(self, directory):
        # type: (str) -> bool
        ldir = directory.lower()
        return ldir.startswith(self._dir.lower())

    def find_active_env(self):
        # type: () -> t.Optional[Env]
        """Finds an activated env."""
        for env in self.list():
            if env.active:
                return env
        return None

    def get(self, managed, name_or_directory):
        # type: (bool, str) -> t.Optional[Env]
        """Grabs a managed Env by name or unmanaged env by directory."""
        if managed:
            name = name_or_directory
            dir_path = os.path.join(self._dir, name_or_directory)
        else:
            dir_path = name_or_directory
            name = os.path.basename(dir_path)
            if self._manages_directory(dir_path):
                # some wise acre passed a directory that's actually managed
                managed = True

        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            toolchain = os.path.join(dir_path, 'cget/cget.cmake')
            if os.path.exists(toolchain) and os.path.isfile(toolchain):
                return Env(name, ct.FilePath(dir_path), managed)
        return None

    def list(self):
        # type: () -> t.List[Env]
        result = []  # type: t.List[Env]

        if CGET_PREFIX and not self._manages_directory(CGET_PREFIX):
            fs_env = Env(os.path.basename(CGET_PREFIX),
                         ct.FilePath(CGET_PREFIX),
                         False)
            result.append(fs_env)
        for file in os.listdir(self._dir):
            dir_path = os.path.join(self._dir, file)
            if os.path.isdir(dir_path):
                result.append(Env(file, ct.FilePath(dir_path), True))

        return result
