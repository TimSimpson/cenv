import os

import typing as t  # NOQA
from . import types as ct  # NOQA


class Options(object):
    def __init__(self):
        self._root_directory = None  # type: t.Optional[ct.FilePath]

    def _from_root(self, path):
        return os.path.join(self._root_directory, path)

    @property
    def environments(self):
        # type: () -> ct.FilePath
        return self._from_root('envs')

    @property
    def toolchains(self):
        return self._from_root('toolchains')
