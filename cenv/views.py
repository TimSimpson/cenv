import abc

import six

import typing as t  # NOQA
from . import types as ct  # NOQA


@six.add_metaclass(abc.ABCMeta)
class View(object):

    # @abc.abstractmethod
    # def add_toolchain(self, toolchain):
    #     # type: (ct.ToolChain) -> None
    #     pass

    # @abc.abstractmethod
    # def create_env(self, env):
    #     # type: (ct.Env) -> None
    #     pass

    @abc.abstractmethod
    def run_command(self, command):
        # type: (str) -> None
        pass


class Silent(View):

    def run_command(self, command):
        # type: (str) -> None
        pass
