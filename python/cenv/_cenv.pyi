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
