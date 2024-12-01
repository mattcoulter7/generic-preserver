import pytest

from typing import (
    TypeVar,
    Generic,
)

from generic_preserver.wrapper import generic_preserver


def test_template():
    A = TypeVar("A")
    B = TypeVar("B")
    C = TypeVar("C")

    class ExampleA: pass
    class ExampleB: pass
    class ExampleC: pass

    @generic_preserver
    class Parent(
        Generic[A, B]
    ): pass

    class Child(
        Parent[ExampleA, B],
        Generic[B, C]
    ): pass

    class GrandChild(
        Child[ExampleB, C],
        Generic[C]
    ): pass

    instance = GrandChild[ExampleC]()

    assert instance[A] is ExampleA
    assert instance[B] is ExampleB
    assert instance[C] is ExampleC

    # check invalid type through a KeyError
    D = TypeVar("D")
    with pytest.raises(KeyError) as exc_info:
        # Code that should raise the exception
        instance[D]
