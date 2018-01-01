import os
import typing as t  # NOQA

import pytest

from .. import path


def test_get_path_seperator(monkeypatch):
    # type: (t.Any) -> None
    monkeypatch.setattr(os, 'name', 'nt')
    assert ';' == path.get_path_seperator()
    monkeypatch.setattr(os, 'name', 'unix')
    assert ':' == path.get_path_seperator()


def make_pu(monkeypatch, seperator, case_sensitive):
    # type: (t.Any, str, bool) -> path.PathUpdater
    monkeypatch.setattr(os, 'name', 'linux' if case_sensitive else 'nt')
    return path.PathUpdater(seperator)


class TestUpdatePaths(object):

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        # type: (t.Any) -> None
        self.mp = monkeypatch

    def make_pu(self, case_sensitive):
        # type: (bool) -> path.PathUpdater
        return make_pu(self.mp, 'does-not-matter', case_sensitive)

    def test_empty(self):
        # type: () -> None
        pu = self.make_pu(True)
        expected = []  # type: t.List
        actual = pu._update_paths([], [], [])
        assert expected == actual

    def test_remove_one(self):
        # type: () -> None
        pu = self.make_pu(True)
        expected = []  # type: t.List
        actual = pu._update_paths(['abc'], old_path=['abc'], new_path=[])
        assert expected == actual

    def test_remove_only_takes_one(self):
        # type: () -> None
        pu = self.make_pu(True)
        # Makes certain we only remove one instance. This is for cases where
        # a user may have activated an environment and caused locations to be
        # added to their path which were already in the path, and we don't
        # want to purge everything.
        expected = ['abc', 'abc']
        actual = pu._update_paths(['abc', 'abc', 'abc'],
                                  old_path=['abc'], new_path=[])
        assert expected == actual

    def test_remove_when_case_sensitive(self):
        # type: () -> None
        pu = self.make_pu(True)
        expected = ['aBC', 'Abc']
        actual = pu._update_paths(['aBC', 'Abc', 'abc'],
                                  old_path=['abc'], new_path=[])
        assert expected == actual

    def test_remove_when_case_insensitive(self):
        # type: () -> None
        pu = self.make_pu(False)
        expected = ['Abc', 'abc']
        actual = pu._update_paths(['aBC', 'Abc', 'abc'],
                                  old_path=['abc'], new_path=[])
        assert expected == actual

    def test_add_one(self):
        # type: () -> None
        pu = self.make_pu(True)
        expected = ['aBc']  # type: t.List
        actual = pu._update_paths([],
                                  old_path=[], new_path=['aBc'])
        assert expected == actual

    def test_add_one_case_insensitive(self):
        # type: () -> None
        pu = self.make_pu(False)
        # Ensure that even on case insensitive platforms the exact string
        expected = ['aBc']  # type: t.List
        actual = pu._update_paths([],
                                  old_path=[], new_path=['aBc'])
        assert expected == actual

    def test_add_one_multiples(self):
        # type: () -> None
        pu = self.make_pu(True)
        expected = ['aBc', 'aBC', 'abc']
        actual = pu._update_paths(['abc'],
                                  old_path=[], new_path=['aBc', 'aBC'])
        assert expected == actual

    def test_add_one_multiples_case_insensitive(self):
        # type: () -> None
        pu = self.make_pu(False)
        expected = ['aBc', 'aBC', 'abc']
        actual = pu._update_paths(['abc'],
                                  old_path=[], new_path=['aBc', 'aBC'])
        assert expected == actual

    def test_add_and_remove(self):
        # type: () -> None
        pu = self.make_pu(False)
        expected = ['fgh', 'abc']
        actual = pu._update_paths(['abc', 'cde'],
                                  old_path=['cde'], new_path=['fgh'])
        assert expected == actual

    def test_add_and_remove_2(self):
        # type: () -> None
        pu = self.make_pu(False)
        expected = ['fgh', '123', 'abc']
        actual = pu._update_paths(['abc', 'cde'],
                                  old_path=['cde'], new_path=['fgh', '123'])
        assert expected == actual


class TestUpdatePathsPublicInterface(object):
    """
    This tests the interface, which allows a string, a list, or None, and
    normalizes all arguments.
    """

    @pytest.fixture(autouse=True)
    def setup(self, monkeypatch):
        # type: (t.Any) -> None
        self.mp = monkeypatch

    def make_pu(self, seperator, case_sensitive):
        # type: (str, bool) -> path.PathUpdater
        return make_pu(self.mp, seperator, case_sensitive)

    def test_does_nothing(self):
        # type: () -> None
        self.mp.delitem(os.environ, 'PATH')
        pu = self.make_pu(':', True)
        expected = ''
        actual = pu.update_paths('PATH')
        assert expected == actual

    def test_pass_none(self):
        # type: () -> None
        self.mp.delitem(os.environ, 'PATH')
        pu = self.make_pu(':', True)
        expected = ''
        actual = pu.update_paths('PATH', None, None)
        assert expected == actual

    def test_removes_one(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'abc:def')
        pu = self.make_pu(':', True)
        expected = 'abc'
        actual = pu.update_paths('PATH', old_path='def')
        assert expected == actual

    def test_removes_two(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'abc:def:ghi')
        pu = self.make_pu(':', True)
        expected = 'def'
        actual = pu.update_paths('PATH', old_path=['ghi', 'abc'])
        assert expected == actual

    def test_removes_only_one(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'AbC;abc;def')
        pu = self.make_pu(';', False)
        expected = 'abc;def'
        actual = pu.update_paths('PATH', old_path='abc')
        assert expected == actual

    def test_removes_only_one_case_sensitive(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'AbC:abc:def')
        pu = self.make_pu(':', True)
        expected = 'AbC:def'
        actual = pu.update_paths('PATH', old_path='abc')
        assert expected == actual

    def test_adds_one(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'abc:def')
        pu = self.make_pu(':', True)
        expected = '123:abc:def'
        actual = pu.update_paths('PATH', new_path='123')
        assert expected == actual

    def test_adds_two(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'abc:def')
        pu = self.make_pu(':', True)
        expected = '123:abc:abc:def'
        actual = pu.update_paths('PATH', new_path=['123', 'abc'])
        assert expected == actual

    def test_removes_matching_paths(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', 'abc:def')
        pu = self.make_pu(':', True)
        expected = 'abc:def'
        actual = pu.update_paths('PATH', ['1', '2'], ['1', '2'])
        assert expected == actual

    def test_removes_matching_paths_2(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', '123:456')
        pu = self.make_pu(':', True)
        expected = 'abC:DeFh:123:456'
        # Note that abC and ABc are treated differently, because it's case
        # sensitive.
        actual = pu.update_paths('PATH', ['abC', 'DeFh'], ['ABc', 'dEf'])
        assert expected == actual

    def test_removes_matching_paths_3(self):
        # type: () -> None
        self.mp.setitem(os.environ, 'PATH', '123;456')
        pu = self.make_pu(';', False)
        expected = 'DeFh;123;456'
        # Unlike above, 'abC' == 'ABc' because it's case insensitive.
        actual = pu.update_paths('PATH', ['abC', 'DeFh'], ['ABc', 'dEf'])
        assert expected == actual
