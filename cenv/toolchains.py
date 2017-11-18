import os
import shutil

import typing as t  # NOQA
from . import types as ct  # NOQA


ToolChain = ct.ToolChain


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

    def delete(self, name):
        # type: (str) -> None
        """Deletes a toolchain."""
        tc = self.get(name)
        if tc is None:
            return
        if os.path.exists(tc.file_path):
            if not tc.file_path.startswith(self._dir):
                raise RuntimeError('ToolChain exists with bad path.')
            os.remove(tc.file_path)

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
