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


def update_paths(paths, new_path, old_path=None):
    # type: (t.List[str], str, t.Optional[str]) -> t.List[str]
    """Given a list of paths, add a new path (and optionally remove old one)"""
    result = list(paths)
    if 'nt' == os.name:
        l_new_path = new_path.lower()
        l_old_path = None if old_path is None else old_path.lower()
        if l_new_path == l_old_path:  # no op
            return result
        l_paths = [p.lower() for p in paths]
        if l_old_path is not None:
            old_path_i = l_paths.index(l_old_path)
            del result[old_path_i]

        if new_path in l_paths:
            return result
        return [new_path] + result
    else:
        if new_path == old_path:
            return result
        if old_path is not None:
            old_path_i = paths.index(old_path)
            del result[old_path_i]
        if new_path in paths:
            return result
        return [new_path] + result
