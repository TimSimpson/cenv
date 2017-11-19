import os

import typing as t  # NOQA

import pytest

from .. import cli
from .. import options
from .. import types as ct  # NOQA


@pytest.fixture
def captured_output(monkeypatch):
    # type: (t.Any) -> t.List[str]
    recorded_output = []  # type: t.List[str]

    def fake_output(text):
        # type: (str) -> None
        recorded_output.append(text)

    monkeypatch.setattr(cli, "output", fake_output)
    return recorded_output


@pytest.fixture
def test_options(monkeypatch, random_directory):
    # type: (t.Any, ct.FilePath) -> options.Options
    ops = options.Options(random_directory)

    def fake_get_options():
        # type: () -> options.Options
        return ops

    monkeypatch.setattr(cli, "get_options", fake_get_options)
    return ops


def test_cli(captured_output, test_options):
    # type: (t.List[str], options.Options) -> None
    os.mkdir(test_options.environments)
    os.mkdir(test_options.toolchains)

    cli.cmd_list([])
    assert ['No envs found!'] == captured_output
    del captured_output[:]

    cli.cmd_create(['typical-env'])
    assert captured_output[0].startswith('Created')
    del captured_output[:]

    cli.cmd_list([])
    assert ['  typical-env'] == captured_output
    del captured_output[:]

    cli.cmd_create(['clang-env', '--cxx', 'clang++-3.8'])
    assert captured_output[0].startswith('Created')
    del captured_output[:]

    cli.cmd_list([])
    assert ['  clang-env', '  typical-env'] == captured_output
    del captured_output[:]
