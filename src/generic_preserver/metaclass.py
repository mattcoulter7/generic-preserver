from typing import Iterable, get_args

from .utils import (
    copy_class_metadata,
    is_generic_type,
)


class GenericMeta(type):
    """
    Custom metaclass to capture generic arguments.

    Usage:

    ```python
    A = TypeVar("A")
    B = TypeVar("B")
    C = TypeVar("C")

    class ExampleA: pass
    class ExampleB: pass
    class ExampleC: pass

    class Parent(
        Generic[A, B],
        metaclass=GenericMeta    # <-- Only need to use in the base super class
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
    def __call__(cls, *args, **kwargs):
        # Check if the class was parameterized
        if not hasattr(cls, "__generic_map__"):
            raise RuntimeError(
                f"Class {cls.__name__} must be parameterized with type arguments using [...] before instantiation."
            )

        return super().__call__(*args, **kwargs)

    def __getitem__(cls, item):
        # establish parameters as an iterable
        type_references = item
        if not isinstance(type_references, Iterable):
            type_references = (type_references, )

        # ensure it is generic
        if not hasattr(cls, "__orig_bases__"):
            raise RuntimeError(
                f"Class `{repr(cls)}` is not a generic, hence parameterized with type arguments using [...]"
            )

        # lookup the generic base
        try:
            generic_base = next(
                base for base in cls.__orig_bases__
                if is_generic_type(base)
            )
        except StopIteration:
            # no generics in this class
            raise RuntimeError(
                f"Unable to find generic argument in class `{repr(cls)}`"
            )

        # lookup required arguments
        type_vars = get_args(generic_base)
        if len(type_vars) != len(type_references):
            raise RuntimeError(
                f"Incorrect number of type parameters passed. Expected ({len(type_vars)}): {repr(type_vars)}, but received ({len(type_references)}): {repr(type_references)}"
            )

        # looking up existing generic map to ensure we still capture
        # generics from super class
        existing_generic_map = cls.__generic_map__ if hasattr(cls, "__generic_map__") else {}

        # create the class wrapper, which stores the generic instances mapped to type vars
        class PreservedGeneric(cls):
            """
            A Special Kind of Generic which preserves the type references passed
            into the generic
            """
            __generic_map__ = existing_generic_map | {
                var: type_ref
                for var, type_ref in zip(type_vars, type_references)
            }

            def __getitem__(self, item):
                """
                Tries to retrieve the type from __generic_map__ if available,
                whilst preserving any other implementations of __getitem__
                """
                # support multi retrieval ExampleA, ExampleB = self[A, B]
                if isinstance(item, Iterable):
                    return tuple(self[child_item] for child_item in item)

                if item in self.__generic_map__:
                    return self.__generic_map__[item]
                
                try:
                    return super().__getitem__(item)
                except AttributeError:
                    raise KeyError(
                        f"No generic type found for generic arg {repr(item)}"
                    )

        copy_class_metadata(PreservedGeneric, cls)

        return PreservedGeneric
