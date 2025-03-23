import os

import typing as t  # NOQA

from cenv import envs
from .. import types as ct  # NOQA


def test_envs_are_empty(random_directory):
    # type: (ct.FilePath) -> None
    manager = envs.Manager(random_directory)
    assert [] == manager.list()
    assert None is manager.get(True, 'anything')


def test_create_envs(resources_directory, random_directory):
    # type: (ct.FilePath, ct.FilePath) -> None
    manager = envs.Manager(random_directory)

    expected_new_dir = ct.FilePath(os.path.join(random_directory, 'js'))

    new_env = manager.create('js', [])
    assert 'js' == new_env.name
    assert expected_new_dir == new_env.directory

    # Appears in list:
    assert ([envs.Env('js', expected_new_dir)] == manager.list())

    # Appears in get:
    got_env = manager.get(True, 'js')
    assert got_env is not None
    assert 'js' == got_env.name
    assert expected_new_dir == got_env.directory

    # Remove environment
    manager.delete('js')

    assert manager.get(True, 'js') is None
    assert [] == manager.list()
