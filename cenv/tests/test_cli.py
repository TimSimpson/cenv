import os

import pytest

import typing as t  # NOQA

from .. import cli
from .. import envs
from .. import options
from .. import types as ct  # NOQA


@pytest.fixture
def test_options(monkeypatch, random_directory):
    # type: (t.Any, ct.FilePath) -> options.Options
    ops = options.Options(random_directory)

    def fake_get_options():
        # type: () -> options.Options
        return ops

    monkeypatch.setattr(cli, "get_options", fake_get_options)
    return ops


class TestCli(object):

    @pytest.fixture(autouse=True)
    def setup(self, test_options):
        # type: (t.Any, options.Options) -> None
        self.old_path = os.environ.get('PATH', '')
        self.old_ldlp = os.environ.get('LD_LIBRARY_PATH', '')
        self.ops = test_options
        if not os.path.exists(self.ops.environments):
            os.mkdir(self.ops.environments)

    def assert_script_files(self, cenv_name, cget_prefix, path,
                            ld_library_path):
        # type: (str, str, str, str) -> None
        cenv_name_line = 'CENV_NAME={}'.format(cenv_name)
        cget_line = 'CGET_PREFIX={}'.format(cget_prefix)

        with open(self.ops.rc_file, 'r') as rc_file:
            rc = rc_file.read()
            assert 'export {}'.format(cenv_name_line) in rc
            assert 'export {}'.format(cget_line) in rc
            assert 'export PATH={}:{}'.format(path, self.old_path) in rc
            assert 'export LD_LIBRARY_PATH={}:{}'.format(
                ld_library_path, self.old_ldlp) in rc

        with open(self.ops.batch_file, 'r') as batch_file:
            batch = batch_file.read()
            assert 'set {}'.format(cenv_name_line) in batch
            assert 'set {}'.format(cget_line) in batch
            assert 'set PATH={};{}'.format(path, self.old_path) in batch
            assert 'set LD_LIBRARY_PATH={};{}'.format(
                ld_library_path, self.old_ldlp) in batch

    def test_cli(self, monkeypatch, captured_output):
        # type: (t.Any, t.List[str]) -> None

        monkeypatch.setattr(envs, 'CGET_PREFIX', '')

        cli.cmd_list([])
        assert ['No envs found!'] == captured_output
        del captured_output[:]

        cli.cmd_init(['typical-env'])
        assert captured_output[0].startswith('Created')
        del captured_output[:]

        cli.cmd_list([])
        assert ['  typical-env'] == captured_output
        del captured_output[:]

        cli.cmd_init(['clang-env', '--cxx', 'clang++-3.8'])
        assert captured_output[0].startswith('Created')
        del captured_output[:]

        cli.cmd_list(['-v'])
        assert ['  clang-env\t--cxx clang++-3.8',
                '  typical-env\t'] == sorted(captured_output)
        del captured_output[:]

        cli.cmd_set(['clang-env'])
        assert ['* * using clang-env'] == sorted(captured_output)
        del captured_output[:]
        self.assert_script_files(
            cenv_name='clang-env',
            cget_prefix=self.ops._from_root('envs/clang-env'),
            path=self.ops._from_root('envs/clang-env/lib'),
            ld_library_path=self.ops._from_root('envs/clang-env/lib'))

        # Normally, the shell integration would set this when the files -
        # which we checked for correctness above - are sourced.
        monkeypatch.setattr(envs,
                            'CGET_PREFIX',
                            self.ops._from_root('envs/clang-env'))

        cli.cmd_list([])
        assert ['* clang-env',
                '  typical-env'] == list(reversed(sorted(captured_output)))
        del captured_output[:]

    def test_init_no_name(self, captured_output):
        # type: (t.List[str]) -> None
        result = cli.cmd_init([])

        assert 1 == result
        assert captured_output[0].startswith('Usage: ')

    def test_init_with_prefix(self, captured_output):
        # type: (t.List[str]) -> None
        result = cli.cmd_init(['cenv-name', '--prefix'])

        assert 1 == result
        assert captured_output[0].startswith('Invalid value `--prefix`')

    def test_init_with_prefix_2(self, captured_output):
        # type: (t.List[str]) -> None
        result = cli.cmd_init(['cenv-name', '-p'])

        assert 1 == result
        assert captured_output[0].startswith('Invalid value `--prefix`')

    def test_set_with_invalid_name(self, captured_output):
        # type: (t.List[str]) -> None
        result = cli.cmd_set(['some-random-name'])

        assert 1 == result
        assert captured_output[0].startswith('No such environment')

    def test_set_with_invalid_directory(self, captured_output):
        # type: (t.List[str]) -> None
        result = cli.cmd_set(['--dir', self.ops._from_root('gfjkghj')])

        assert 1 == result
        assert 'not a directory or does not contain a' in captured_output[0]
