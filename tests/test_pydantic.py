import pytest
from abc import ABC, abstractmethod

from pydantic import BaseModel, ValidationError

from generic_preserver.wrapper import generic_preserver

from typing import Generic, TypeVar


def test():
    A = TypeVar("A")
    B = TypeVar("B")
    C = TypeVar("C")
    D = TypeVar("D")

    class ExampleA(BaseModel): ...
    class ExampleB(BaseModel): ...
    class ExampleC(BaseModel): ...

    @generic_preserver
    class Parent(BaseModel, Generic[A, B], ABC):
        # sample field using the type parameter A
        sample: A
        meta: B | None = None

        @property
        def a_type(self):  # noqa: N802
            return self[A]

        @property
        def b_type(self):  # noqa: N802
            return self[B]

        @abstractmethod
        def do_something(self) -> str:
            ...

    class Child(Parent[ExampleA, B], Generic[B, C]):
        child_extra: C

        @property
        def c_type(self):  # noqa: N802
            return self[C]

        def do_something(self) -> str:
            return "ok"

    class GrandChild(Child[ExampleB, C], Generic[C]):
        pass

    # instantiate a fully specialised Pydantic model
    instance = GrandChild[ExampleC](
        sample=ExampleA(),
        meta=ExampleB(),
        child_extra=ExampleC(),
    )

    # check single type extraction via properties
    assert instance.a_type is ExampleA
    assert instance.b_type is ExampleB
    assert instance.c_type is ExampleC

    # check the underlying generic map is fully flattened
    assert instance.__generic_map__ == {
        "A": ExampleA,
        "B": ExampleB,
        "C": ExampleC,
    }

    # invalid lookup still raises KeyError
    with pytest.raises(KeyError):
        instance[TypeVar("E")]  # new, unrelated TypeVar

    # --- generic-of-generic case with BaseModel -------------------

    class ExampleD(BaseModel, Generic[D]):
        value: D

    class ConcreteParent(Parent[ExampleA, ExampleD[ExampleB]]):
        def do_something(self) -> str:
            return "ok"

    instance_2 = ConcreteParent(
        sample=ExampleA(),
        meta=ExampleD[ExampleB](value=ExampleB()),
    )

    assert instance_2.a_type is ExampleA
    assert instance_2.b_type is ExampleD[ExampleB]
    assert instance_2[A, B] == (
        ExampleA,
        ExampleD[ExampleB],
    )

    # --- validation error checks ---------------------------------

    # 1) Wrong type for `sample` (expects ExampleA, gets a plain string)
    with pytest.raises(ValidationError):
        GrandChild[ExampleC](
            sample="not ExampleA",
            meta=ExampleB(),
            child_extra=ExampleC(),
        )

    # 2) Wrong nested type for ExampleD[ExampleB].value
    with pytest.raises(ValidationError):
        ConcreteParent(
            sample=ExampleA(),
            meta=ExampleD[ExampleB](value="not ExampleB"),
        )
