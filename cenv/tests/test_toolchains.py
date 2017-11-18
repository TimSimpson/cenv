import os

import typing as t  # NOQA

from cenv import toolchains
from .. import types as ct  # NOQA


def test_toolchain_is_empty(random_directory):
    # type: (ct.FilePath) -> None
    manager = toolchains.Manager(random_directory)
    assert [] == manager.list()
    assert None is manager.get('anything')


def test_toolchain_create(resources_directory, random_directory):
    # type: (ct.FilePath, ct.FilePath) -> None
    manager = toolchains.Manager(random_directory)
    toolchain_file = ct.FilePath(
        os.path.join(resources_directory, 'Emscripten.cmake'))

    expected_new_tc_file = os.path.join(random_directory, 'emscripten')

    new_tc = manager.add_from_file('emscripten', toolchain_file)
    assert 'emscripten' == new_tc.name
    assert expected_new_tc_file == new_tc.file_path

    # Appears in list:
    assert ([toolchains.ToolChain(
                'emscripten', ct.FilePath(expected_new_tc_file))]
            == manager.list())

    # Appears in get
    got_tc = manager.get('emscripten')
    assert got_tc is not None
    assert 'emscripten' == got_tc.name
    assert expected_new_tc_file == got_tc.file_path
