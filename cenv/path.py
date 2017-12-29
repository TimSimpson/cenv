"""Manipulates path."""
import os

import typing as t  # NOQA


def get_path_seperator():
    # type: () -> str
    """Returns character that seperates directories in the PATH env variable"""
    if 'nt' == os.name:
        return ';'
    else:
        return ':'


class PathUpdater(object):

    def __init__(self, path_seperator):
        # type: (str) -> None
        self._path_seperator = path_seperator

    def get_paths(self):
        # type: () -> t.List[str]
        """Gets the paths from the PATH env variable."""
        env_path = os.environ['PATH']
        paths = env_path.split(self._path_seperator)
        return paths

    def set_paths(self, paths):
        # type: (t.List[str]) -> str
        """Turns a list of paths back into a path string and sets env var."""
        new_path = self._path_seperator.join(paths)
        os.environ['PATH'] = new_path
        return new_path

    def update_paths(self, path_var_name, new_path=None, old_path=None):
        # type: (str, t.Optional[str], t.Optional[str]) -> str
        """
        Given the name of an environment variables that stores a list of paths,
        return a value where, optionally one path is added and optionally one
        may be removed. Also updates the environment variable.
        """
        original_value = os.environ.get(path_var_name, '')
        original_list = original_value.split(self._path_seperator)
        modified_list = self._update_paths(original_list, new_path, old_path)
        modified_value = self._path_seperator.join(modified_list)
        return modified_value

    def _update_paths(self, paths, new_path=None, old_path=None):
        # type: (t.List[str], t.Optional[str], t.Optional[str]) -> t.List[str]
        """Takes list of paths, adds a path (and optionally removes old one)"""
        result = list(paths)
        if 'nt' == os.name:
            l_new_path = None if new_path is None else new_path.lower()
            l_old_path = None if old_path is None else old_path.lower()
            if l_new_path == l_old_path:  # no op
                return result
            l_paths = [p.lower() for p in paths]
            if l_old_path is not None:
                old_path_i = l_paths.index(l_old_path)
                del result[old_path_i]

            if l_new_path is None or l_new_path in l_paths:
                return result

            assert new_path is not None
            return [new_path] + result
        else:
            if new_path == old_path:
                return result
            if old_path is not None:
                try:
                    old_path_i = paths.index(old_path)
                    del result[old_path_i]
                except ValueError:
                    # This happens if the old_path wasn't found, which occurs
                    # in some odd cases (such as testing)
                    pass
            if new_path is None or new_path in paths:
                return result
            return [new_path] + result
