from __future__ import annotations

from typing import Any

from .utils import canonical_key

try:
    from pydantic import BaseModel as PydanticBaseModel
except ImportError:
    PydanticBaseModel = None


def specialise_pydantic_generic(cls: type, item: Any) -> type[PydanticBaseModel] | None:
    """
    If `cls` is a Pydantic BaseModel subclass, let Pydantic perform the
    generic specialisation, then attach/extend `__generic_map__` on the
    specialised model.

    Returns the specialised subclass, or `None` if:

    - pydantic isn't installed, or
    - `cls` is not a Pydantic BaseModel subclass.
    """
    if PydanticBaseModel is None:
        return None

    if not isinstance(cls, type) or not issubclass(cls, PydanticBaseModel):
        return None

    # Let Pydantic create the specialised generic model
    submodel = cls.__class_getitem__(item)  # type: ignore[attr-defined]

    # Pydantic stores its generic info in `__pydantic_generic_metadata__`
    meta_sub = getattr(submodel, "__pydantic_generic_metadata__", {}) or {}
    origin = meta_sub.get("origin") or cls

    origin_meta = getattr(origin, "__pydantic_generic_metadata__", {}) or {}
    params = origin_meta.get("parameters") or getattr(origin, "__parameters__", ())

    # Concrete type arguments – prefer what's already in the metadata
    args = meta_sub.get("args")
    if not args:
        args = item if isinstance(item, tuple) else (item,)

    existing_generic_map = getattr(cls, "__generic_map__", {})

    def resolve_type_reference(ref: Any) -> Any:
        """
        If the argument is itself a type parameter that has already been
        mapped upstream, resolve via `existing_generic_map`.
        """
        key = canonical_key(ref)
        return existing_generic_map.get(key, ref)

    new_entries = {
        canonical_key(param): resolve_type_reference(arg)
        for param, arg in zip(params, args)
    }

    merged = {**existing_generic_map, **new_entries}
    setattr(submodel, "__generic_map__", merged)

    # Attach instance-level __getitem__ once so you can do: instance[A], instance[B], ...
    if "_generic_preserver_instance_getitem" not in submodel.__dict__:

        def _instance_getitem(self, key: Any):
            if isinstance(key, tuple):
                return tuple(self[k] for k in key)

            k = canonical_key(key)
            generic_map = getattr(self.__class__, "__generic_map__", {})
            if k in generic_map:
                return generic_map[k]

            raise KeyError(f"No generic type found for generic arg {repr(key)}")

        setattr(submodel, "_generic_preserver_instance_getitem", _instance_getitem)

        # Only define __getitem__ if the model doesn't already define one
        if "__getitem__" not in submodel.__dict__:
            submodel.__getitem__ = _instance_getitem  # type: ignore[assignment]

    return submodel
