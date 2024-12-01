from typing import (
    Type,
    List,
    Optional,
)


def get_metaclasses(
    cls: Type,
    seen=None
) -> List[Type]:
    """
    Retrieves a list of metaclasses used by cls and its base classes,
    preserving order and avoiding duplicates.

    Parameters:
        cls (type): The class from which to retrieve metaclasses.
        seen (set): A set to track seen metaclasses (used internally).

    Returns:
        List[type]: A list of metaclass types.
    """
    if seen is None:
        seen = set()

    metaclasses = []
    for base in cls.__bases__:
        base_meta = type(base)
        if base_meta not in seen:
            seen.add(base_meta)
            metaclasses.append(base_meta)
            # Recursively collect metaclasses from base classes
            metaclasses.extend(
                m for m in get_metaclasses(base, seen) if m not in seen
            )

    return metaclasses


def build_combined_metaclass(
    metaclasses: List[Type],
) -> Type:
    """
    Creates a combined metaclass from a list of metaclasses.

    Parameters:
        metaclasses (List[type]): A list of metaclass types.

    Returns:
        type: A combined metaclass that inherits from all provided metaclasses.

    Raises:
        TypeError: If the metaclasses cannot be combined due to incompatibility.
    """
    # Remove duplicates while preserving order and exclude 'type'
    seen = set()
    metaclasses = [
        m for m in metaclasses
        if (
            m not in seen
            and not seen.add(m)
            and m is not type
        )
    ]

    # If there's only one metaclass, return it directly
    if len(metaclasses) == 1:
        return metaclasses[0]

    # Attempt to create a combined metaclass
    try:
        # The name 'CombinedMeta' is arbitrary and can be adjusted
        return type(
            'CombinedMeta',
            tuple(metaclasses),
            {}
        )

    except TypeError as e:
        # Metaclass conflict occurred
        raise TypeError(
            f"Cannot create a combined metaclass from {metaclasses}: {e}"
        ) from e


def build_combined_metaclass_from_cls(
    cls: Type,
    *,
    custom_metaclasses: Optional[List[Type]] = None,
) -> Type:
    """
    Creates a combined metaclass from class and a list of additiona metaclasses.

    Parameters:
        cls (type): this class which base metaclasses will be looked up from.
        metaclasses (List[type]): A list of additional metaclass types.

    Returns:
        type: A combined metaclass that inherits from all provided metaclasses.

    Raises:
        TypeError: If the metaclasses cannot be combined due to incompatibility.
    """
    # get metaclasses for the provided class
    metaclasses = get_metaclasses(cls)

    # combine with any custom metaclasses
    if custom_metaclasses is not None:
        metaclasses = custom_metaclasses + metaclasses

    # build the combined metalclass
    CombinedMetaclass = build_combined_metaclass(metaclasses)

    return CombinedMetaclass
