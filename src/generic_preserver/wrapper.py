from __future__ import annotations

from typing import TypeVar

from .metaclass import GenericMeta
from .utils import copy_class_metadata
from .conflict_management import build_combined_metaclass_from_cls

T = TypeVar("T", bound=type)


def generic_preserver(cls: T) -> T:
    """
    A decorator that enables capturing generic arguments.
    _(Skips needing to provide the explicit `metaclass=GenericMeta` parameter in class definition)_.

    Works with:
    - Classic TypeVar + Generic[...] style, and
    - PEP 695: `class Parent[A, B]: ...`

    Also supports Pydantic BaseModel subclasses by *opting out* of
    Pydantic's own generic param tracking, so that our GenericMeta
    is the only thing responsible for generics here.
    """
    CombinedMetaclass = build_combined_metaclass_from_cls(
        cls,
        custom_metaclasses=[GenericMeta],
    )

    # Root wrapper with combined metaclass
    class Wrapped(cls, metaclass=CombinedMetaclass):
        __generic_preserver_root__ = True

        def __init_subclass__(subcls, **kwargs):
            # Let Pydantic / ABC / user code run their normal hooks first
            super().__init_subclass__(**kwargs)

            # --- Pydantic compatibility for *all subclasses* ---
            # If this subclass is a Pydantic model with generic metadata,
            # blank out its parameters so Pydantic doesn't enforce its own
            # Generic[...] parameter consistency across this hierarchy.
            # pmeta = getattr(subcls, "__pydantic_generic_metadata__", None)
            # if isinstance(pmeta, dict) and "parameters" in pmeta:
            #     new_meta = dict(pmeta)
            #     new_meta["parameters"] = ()
            #     subcls.__pydantic_generic_metadata__ = new_meta
            # ---------------------------------------------------

    copy_class_metadata(Wrapped, cls)

    # --- Pydantic compatibility for the *root* itself ------------
    # If the root is already a Pydantic model with generic metadata,
    # clear its parameters too; this prevents the first child from
    # triggering the "All parameters must be present on typing.Generic"
    # error when Pydantic compares parent vs child parameters.
    # root_meta = getattr(Wrapped, "__pydantic_generic_metadata__", None)
    # if isinstance(root_meta, dict) and "parameters" in root_meta:
    #     new_root_meta = dict(root_meta)
    #     # new_root_meta["parameters"] = ()
    #     Wrapped.__pydantic_generic_metadata__ = new_root_meta
    # -------------------------------------------------------------

    return Wrapped  # type: ignore[return-value]
