from cenv import types as ct
import typing as t


class Options:
    def __init__(self, root_directory: ct.FilePath) -> None:
        ...

    @property
    def batch_file(self) -> ct.FilePath:
        ...

    @property
    def environments(self) -> ct.FilePath:
        ...

    @property
    def rc_file(self) -> ct.FilePath:
        ...

    @property
    def root_directory(self) -> ct.FilePath:
        ...

    def _from_root(self, path: t.Union[str, ct.FilePath]) -> ct.FilePath:
        ...

def get_path_seperator() -> str:
    ...

class PathUpdater(object):

    def __init__(self, path_seperator: str) -> None:
        ...


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
