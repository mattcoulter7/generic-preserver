"""Testing compatibility with python Generics >=3.12."""

import pytest

from generic_preserver.wrapper import generic_preserver


def test():
    class ExampleA: ...
    class ExampleB: ...
    class ExampleC: ...

    @generic_preserver
    class Parent[A, B]:
        @property
        def a(self):  # noqa: N802
            return self[A]

        @property
        def b(self):  # noqa: N802
            return self[B]

    class Child[B, C](Parent[ExampleA, B]):
        @property
        def c(self):  # noqa: N802
            return self[C]

    class GrandChild[C](Child[ExampleB, C]):
        pass

    instance = GrandChild[ExampleC]()

    # check single type extraction (via properties)
    assert instance.a is ExampleA
    assert instance.b is ExampleB
    assert instance.c is ExampleC

    # With PEP-695, we no longer have global type vars. This first
    # caused issues as under-the-hood, generic preservver would see
    # 2 different B TypeVars, where previously they would be the same
    # global instance.
    #
    # To support this, generic preserver now computes a canonical key
    # using TypeVar(...).__name__, which in turn allows us to access the
    # instances via a string.
    #
    # I don't recommend this, as the property approach keeps things clean
    # but the test ensures that it is in fact working.
    assert instance["A", "B", "C"] == (ExampleA, ExampleB, ExampleC)

    # check invalid type through a KeyError
    class D:  # sentinel type key that should not exist
        pass

    with pytest.raises(KeyError):
        instance[D]

    # check generic of generic
    class ExampleD[D]: ...

    instance_2 = Parent[ExampleA, ExampleD[ExampleB]]()

    assert instance_2.a is ExampleA
    assert instance_2.b is ExampleD[ExampleB]
    assert instance_2["A", "B"] == (ExampleA, ExampleD[ExampleB])
