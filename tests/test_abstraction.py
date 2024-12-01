import pytest

from typing import (
    TypeVar,
    Generic,
)
from abc import ABC

from generic_preserver.wrapper import generic_preserver


def test_template():
    T = TypeVar("T")

    class ExampleT: pass

    @generic_preserver
    class AbstractBase(
        Generic[T],
        ABC
    ): pass

    class Variant1(AbstractBase[ExampleT]): pass

    instance = Variant1()

    assert instance[T] is ExampleT

    pass
