import typing as t  # NOQA

from cenv import envs
from .. import types as ct  # NOQA


def test_envs_are_empty(random_directory):
    # type: (ct.FilePath) -> None
    manager = envs.Manager(random_directory)
    assert [] == manager.list()
    assert None is manager.get('anything')
