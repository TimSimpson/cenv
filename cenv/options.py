import os

import typing as t  # NOQA
from . import types as ct  # NOQA


class Options(object):
    def __init__(self, root_directory):
        # type: (ct.FilePath) -> None
        self._root_directory = root_directory  # type: ct.FilePath

    def _from_root(self, path):
        # type: (t.Union[str, ct.FilePath]) -> ct.FilePath
        assert self._root_directory is not None
        return ct.FilePath(os.path.join(self._root_directory, path))

    @property
    def batch_file(self):
        # type: () -> ct.FilePath
        return self._from_root("set-vars.bat")

    @property
    def environments(self):
        # type: () -> ct.FilePath
        return self._from_root("envs")

    @property
    def rc_file(self):
        # type: () -> ct.FilePath
        return self._from_root("cenv.rc")
