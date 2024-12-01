from typing import _GenericAlias


def is_generic_type(obj) -> bool:
    # Check for built-in generics
    return isinstance(obj, _GenericAlias)


def copy_class_metadata(wrapped, original) -> None:
    """Copy relevant metadata from the original class to the wrapped class."""
    wrapped.__doc__ = original.__doc__
    wrapped.__name__ = original.__name__
    wrapped.__annotations__ = getattr(original, '__annotations__', {})
    wrapped.__module__ = getattr(original, '__module__', None)
    wrapped.__qualname__ = getattr(original, '__qualname__', None)

    return None
