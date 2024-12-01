from .metaclass import GenericMeta
from .utils import (
    copy_class_metadata,
)
from .conflict_management import (
    build_combined_metaclass_from_cls,
)


def generic_preserver(cls):
    """
    A decorator that enables capturing generic arguments.
    _(Skips needing to provide the explicit `metaclass=GenericMeta` parameter in class definition)_

    Usage:

    ```python
    A = TypeVar("A")
    B = TypeVar("B")
    C = TypeVar("C")

    class ExampleA: pass
    class ExampleB: pass
    class ExampleC: pass

    @generic_preserver  # <-- Only need to use in the base super class
    class Parent(
        Generic[A, B]
    ):
        pass

    class Child(
        Parent[ExampleA, B],
        Generic[B, C]
    ): pass

    class GrandChild(
        Child[ExampleB, C],
        Generic[C]
    ): pass

    instance = GrandChild[ExampleC]()

    print(instance[A])
    >> <class '__main__.ExampleA'>

    print(instance[B])
    >> <class '__main__.ExampleB'>

    print(instance[C])
    >> <class '__main__.ExampleC'>

    print(instance.__generic_map__)
    >> {
        ~A: <class '__main__.ExampleA'>,
        ~B: <class '__main__.ExampleB'>,
        ~C: <class '__main__.ExampleC'>,
    }

    print(instance[D])
    >> KeyError(...)
    ```
    """
    # avoid conflict by dynamically creating a metaclass that
    # groups its base metaclasses (if necessary)
    CombinedMetaclass = build_combined_metaclass_from_cls(
        cls,
        custom_metaclasses=[GenericMeta],
    )
    
    # Dynamically create a new class using the GenericMeta metaclass
    class Wrapped(cls, metaclass=CombinedMetaclass):
        ...

    copy_class_metadata(Wrapped, cls)

    return Wrapped
