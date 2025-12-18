from typing import Any, _GenericAlias


def is_generic_type(obj) -> bool:
    # Check for built-in generics
    return isinstance(obj, _GenericAlias)


def copy_class_metadata(wrapped, original) -> None:
    """Copy relevant metadata from the original class to the wrapped class."""
    wrapped.__doc__ = original.__doc__
    wrapped.__name__ = original.__name__
    wrapped.__annotations__ = getattr(original, "__annotations__", {})
    wrapped.__module__ = getattr(original, "__module__", None)
    wrapped.__qualname__ = getattr(original, "__qualname__", None)

    return None


def canonical_key(tp: Any) -> Any:
    """
    Produce a stable key for a type parameter or type reference.

    - For TypeVar / PEP 695 type parameters: use their name (`.__name__`).
    - For other objects: use the object itself.

    This allows us to unify separate TypeVar instances that share the same
    logical name (e.g. multiple `B` parameters across an inheritance chain).
    """
    name = getattr(tp, "__name__", None)
    return name if name is not None else tp
