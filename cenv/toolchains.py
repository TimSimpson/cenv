import os
import shutil

import typing as t  # NOQA
from . import types as ct  # NOQA


class ToolChain(object):

    def __init__(self, name, file_path):
        # type: (str, ct.FilePath) -> None
        self._name = name
        self._file_path = file_path

    @property
    def file_path(self):
        # type: () -> ct.FilePath
        return self._file_path

    @property
    def name(self):
        # type: () -> str
        return self._name

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, ToolChain):
            return False
        return all((self._name == other._name,
                    self._file_path == other._file_path))

    def __repr__(self):
        # type: () -> str
        return "(name={}, file_path={})".format(self._name, self._file_path)


class Manager(object):

    def __init__(self, tc_dir):
        # type: (ct.FilePath) -> None
        self._dir = tc_dir  # type: ct.FilePath

    def add_from_file(self, name, file_path):
        # type: (str, ct.FilePath) -> ToolChain
        """Copies the given file into the toolchain directory."""
        if self.get(name) is not None:
            raise ValueError("Toolchain {} already exists!".format(name))

        new_file = os.path.join(self._dir, name)
        if not os.path.exists(file_path):
            raise ValueError("File not found: {}".format(file_path))
        if not os.path.isfile(file_path):
            raise ValueError("Is not a file: {}".format(file_path))

        shutil.copyfile(file_path, new_file)

        return ToolChain(name, ct.FilePath(new_file))

    def get(self, name):
        # type: (str) -> t.Optional[ToolChain]
        """Grabs a toolchain by name."""
        file_path = os.path.join(self._dir, name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return ToolChain(name, ct.FilePath(file_path))
        return None

    def list(self):
        # type: () -> t.List[ToolChain]
        result = []  # type: t.List[ToolChain]
        for file in os.listdir(self._dir):
            file_path = os.path.join(self._dir, file)
            if os.path.isfile(file_path):
                result.append(ToolChain(file, ct.FilePath(file_path)))

        return result
