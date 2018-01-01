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
        self._case_sensitive = 'nt' != os.name

    def _arg_to_list(self, path):
        # type: (t.Union[str, t.List[str], None]) -> t.List[str]
        if not path:
            return []
        elif isinstance(path, str):
            return [path]
        else:
            return [p for p in path]

    def _normalize_path_value(self, path):
        # type: (str) -> str
        """Makes path lower case on Windows, stays the same otherwise."""
        if self._case_sensitive:
            return path
        else:
            return path.lower()

    def _normalize_path_arg(self, path_arg):
        # type: (t.Union[str, t.List[str], None]) -> t.List[str]
        return [self._normalize_path_value(p)
                for p in self._arg_to_list(path_arg)]

    def _remove_matching_elements(self, new_path, old_path):
        # type: (t.Union[str, t.List[str], None], t.Union[str, t.List[str], None]) -> t.Tuple[t.List[str], t.List[str]]  # NOQA
        """Removes elements found in both lists, preserves order."""
        norm_old_path = self._normalize_path_arg(old_path)
        new_path_list = self._arg_to_list(new_path)
        norm_new_path = [self._normalize_path_value(p) for p in new_path_list]
        for i in range(len(norm_old_path)):
            while i < len(norm_old_path) and norm_old_path[i] in norm_new_path:
                while norm_old_path[i] in norm_new_path:
                    delete_index = norm_new_path.index(norm_old_path[i])
                    del norm_new_path[delete_index]
                    del new_path_list[delete_index]
                del norm_old_path[i]
        return new_path_list, norm_old_path

    def update_paths(self, path_var_name, new_path=None, old_path=None):
        # type: (str, t.Union[str, t.List[str], None], t.Union[str, t.List[str], None]) -> str  # NOQA
        """
        Given the name of an environment variables that stores a list of paths,
        return a value where, optionally one path is added and optionally one
        may be removed. Also updates the environment variable.
        """
        new_path, old_path = self._remove_matching_elements(
            new_path,
            old_path)

        original_value = os.environ.get(path_var_name, '')
        original_list = original_value.split(self._path_seperator)

        modified_list = self._update_paths(original_list, new_path, old_path)

        modified_value = self._path_seperator.join(modified_list)
        return modified_value

    def _update_paths(self, original_list, new_path, old_path):
        # type: (t.List[str], t.List[str], t.List[str]) -> t.List
        lc_list = [self._normalize_path_value(e) for e in original_list]

        remove_indices = []  # type: t.List[int]
        for op in old_path:
            if op in lc_list:
                # Remove only once
                remove_indices.append(lc_list.index(op))

        filtered_list = [original_list[i] for i in range(len(original_list))
                         if i not in remove_indices]

        modified_list = new_path + filtered_list

        return modified_list
