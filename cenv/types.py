import typing as t


FilePath = t.NewType('FilePath', str)


class Env(object):

    def __init__(self, name, directory):
        # type: (str, FilePath) -> None
        self._name = name
        self._directory = directory

    @property
    def name(self):
        # type: () -> str
        return self._name

    @property
    def directory(self):
        # type: () -> FilePath
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


class ToolChain(object):

    def __init__(self, name, file_path):
        # type: (str, FilePath) -> None
        self._name = name
        self._file_path = file_path

    @property
    def name(self):
        # type: () -> str
        return self._name

    @property
    def file_path(self):
        # type: () -> FilePath
        return self._file_path

    def __eq__(self, other):
        # type: (object) -> bool
        if not isinstance(other, ToolChain):
            return False
        return all((self._name == other._name,
                    self._file_path == other._file_path))

    def __repr__(self):
        # type: () -> str
        return "ToolChain(name={}, file_path={})".format(
            self._name, self._file_path)
