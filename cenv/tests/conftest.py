import os
import shutil
import uuid

import pytest

import typing as t  # NOQA
from .. import types as ct  # NOQA


@pytest.fixture(scope="session")
def resources_directory():
    # type: () -> ct.FilePath
    """Returns the resources directory.

    This directory contains pre-existing files, checked into version control,
    which are not modified by the tests.
    """
    this_directory = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(this_directory, '../../resources')

    return ct.FilePath(resources_dir)


@pytest.fixture(scope="session")
def test_directory():
    # type: () -> ct.FilePath
    """Creates a directory the tests will mess with.

    At the start of the test run, any files in the test directory are deleted.
    However, no files are deleted when the tests end to make it easier to see
    the results of the last test run.
    """
    this_directory = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(this_directory, '../../output')

    # This directory should already exist. It's part of the git repo.
    assert os.path.isdir(output_dir)
    assert os.path.exists(output_dir)

    test_dir = os.path.join(output_dir, 'test')

    if os.path.exists(test_dir):
        assert os.path.isdir(test_dir)
        shutil.rmtree(test_dir)

    os.mkdir(test_dir)
    return ct.FilePath(test_dir)


@pytest.fixture()
def random_directory(test_directory):
    # type: (ct.FilePath) -> ct.FilePath
    """Just a temp directory."""
    random_dir = os.path.join(test_directory, str(uuid.uuid4()))
    os.mkdir(random_dir)
    return ct.FilePath(random_dir)
