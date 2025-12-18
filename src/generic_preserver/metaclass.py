from typing import get_args
from typing import Any
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
        if not isinstance(type_references, tuple):
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
        except StopIteration as e:
            # no generics in this class
            raise RuntimeError(
                f"Unable to find generic argument in class `{repr(cls)}`"
            ) from e

        # lookup required arguments
        type_vars = get_args(generic_base)
        if len(type_vars) != len(type_references):
            raise RuntimeError(
                f"Incorrect number of type parameters passed. Expected ({len(type_vars)}): {repr(type_vars)}, but received ({len(type_references)}): {repr(type_references)}"
            )

        # looking up existing generic map to ensure we still capture
        # generics from super class
        existing_generic_map = getattr(cls, "__generic_map__", {})

        def canonical_key(tp: Any) -> Any:
            """
            Produce a stable key for a type parameter.

            - For TypeVar / PEP 695 type parameters: use their name
              (`.__name__` or `.name`).
            - For non-type-parameters: just use the object itself.
            """
            name = getattr(tp, "__name__", None)
            return name if name is not None else tp

        def resolve_type_reference(ref: Any) -> Any:
            """
            If the type argument is itself a type parameter that already has
            a concrete binding in `existing_generic_map`, return that binding.

            This is the critical bit that fixes your PEP 695 issue where
            `B` was ending up bound to *another* type parameter instead of the
            final concrete type.
            """
            key = canonical_key(ref)
            return existing_generic_map.get(key, ref)

        # Build the new mapping for this specialisation
        new_entries = {
            canonical_key(param): resolve_type_reference(type_ref)
            for param, type_ref in zip(type_vars, type_references)
        }

        # Create the specialised class that remembers all resolved bindings
        class PreservedGeneric(cls):
            """
            A specialised generic that preserves the type arguments in
            `__generic_map__`.
            """
            __generic_map__ = {**existing_generic_map, **new_entries}

            def __getitem__(self, item: Any):
                """
                Resolve generic parameters from `__generic_map__`, with support
                for multi-lookup: `self[A, B]`.
                """
                # Support e.g. ExampleA, ExampleB = self[A, B]
                if isinstance(item, tuple):
                    return tuple(self[child_item] for child_item in item)

                key = canonical_key(item)

                if key in self.__generic_map__:
                    return self.__generic_map__[key]

                # Fall back to other __getitem__ implementations, if any
                try:
                    return super().__getitem__(item)
                except AttributeError as e:
                    raise KeyError(
                        f"No generic type found for generic arg {repr(item)}"
                    ) from e

        # Preserve basic metadata (name, qualname, etc.)
        copy_class_metadata(PreservedGeneric, cls)

        return PreservedGeneric