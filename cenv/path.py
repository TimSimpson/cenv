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


def get_paths():
    # type: () -> t.List[str]
    """Gets the paths from the PATH env variable."""
    env_path = os.environ['PATH']
    paths = env_path.split(get_path_seperator())
    return paths


def set_paths(paths):
    # type: (t.List[str]) -> str
    """Turns a list of paths back into a path string. Also sets the env var."""
    new_path = get_path_seperator().join(paths)
    os.environ['PATH'] = new_path
    return new_path


def update_paths(path_var_name, new_path=None, old_path=None):
    # type: (str, t.Optional[str], t.Optional[str]) -> str
    """
    Given the name of an environment variables that stores a list of paths,
    return a value where, optionally one path is added and optionally one
    may be removed. Also updates the environment variable.
    """
    original_value = os.environ.get(path_var_name, '')
    original_list = original_value.split(get_path_seperator())
    modified_list = _update_paths(original_list, new_path, old_path)
    modified_value = get_path_seperator().join(modified_list)
    os.environ[path_var_name] = modified_value
    return modified_value


def _update_paths(paths, new_path=None, old_path=None):
    # type: (t.List[str], t.Optional[str], t.Optional[str]) -> t.List[str]
    """Given a list of paths, add a new path (and optionally remove old one)"""
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
            old_path_i = paths.index(old_path)
            del result[old_path_i]
        if new_path is None or new_path in paths:
            return result
        return [new_path] + result
