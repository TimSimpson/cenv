from typing import Optional  # NOQA
from . import types as t  # NOQA


class Options(object):
    def __init__(self):
        self._root_directory = None  # type: Optional[t.FilePath]
