import pytest
from abc import ABC

from typing import (
    Annotated,
    Generic,
    Literal,
    TypeVar,
    Union,
)

from pydantic import BaseModel, Field, ValidationError

from generic_preserver.wrapper import generic_preserver


def test_discriminated_union_with_generic_envelope():
    A = TypeVar("A")
    B = TypeVar("B")

    class UserPayload(BaseModel):
        user_id: int
        name: str

    class SystemPayload(BaseModel):
        message: str
        code: int

    class UserMeta(BaseModel):
        source: str

    class SystemMeta(BaseModel):
        severity: int

    @generic_preserver
    class Envelope(BaseModel, Generic[A, B], ABC):
        kind: str
        payload: A
        meta: B

        @property
        def payload_type(self):  # noqa: N802
            return self[A]

        @property
        def meta_type(self):  # noqa: N802
            return self[B]

    class UserEvent(Envelope[UserPayload, UserMeta]):
        kind: Literal["user"]

    class SystemEvent(Envelope[SystemPayload, SystemMeta]):
        kind: Literal["system"]

    Event = Annotated[
        Union[UserEvent, SystemEvent],
        Field(discriminator="kind"),
    ]

    class EventWrapper(BaseModel):
        event: Event

    # ------------------------------------------------------------------
    # 1) Create a UserEvent, wrap, dump, and validate back
    # ------------------------------------------------------------------
    original_user = EventWrapper(
        event=UserEvent(
            kind="user",
            payload=UserPayload(user_id=1, name="Alice"),
            meta=UserMeta(source="frontend"),
        )
    )

    dumped_user = original_user.model_dump()
    restored_user = EventWrapper.model_validate(dumped_user)

    # Discriminator + union resolution
    assert isinstance(restored_user.event, UserEvent)
    assert dumped_user["event"]["kind"] == "user"

    # Data round-trip
    assert restored_user.event.payload == original_user.event.payload
    assert restored_user.event.meta == original_user.event.meta

    # Generic-preserver mapping + lookup
    assert restored_user.event.__generic_map__ == {
        "A": UserPayload,
        "B": UserMeta,
    }
    assert restored_user.event.payload_type is UserPayload
    assert restored_user.event.meta_type is UserMeta
    assert restored_user.event.payload_type is UserPayload
    assert (
        restored_user.event.payload_type,
        restored_user.event.meta_type,
    ) == (UserPayload, UserMeta)

    # ------------------------------------------------------------------
    # 2) Validate a SystemEvent from raw data (deserialise first)
    # ------------------------------------------------------------------
    raw_system = {
        "event": {
            "kind": "system",
            "payload": {"message": "down", "code": 503},
            "meta": {"severity": 2},
        }
    }

    restored_system = EventWrapper.model_validate(raw_system)

    assert isinstance(restored_system.event, SystemEvent)
    assert restored_system.event.__generic_map__ == {
        "A": SystemPayload,
        "B": SystemMeta,
    }
    assert restored_system.event.payload_type is SystemPayload
    assert restored_system.event.meta_type is SystemMeta

    # ------------------------------------------------------------------
    # 3) A couple of validation error checks
    # ------------------------------------------------------------------
    # Wrong discriminator
    with pytest.raises(ValidationError):
        EventWrapper.model_validate(
            {
                "event": {
                    "kind": "unknown",
                    "payload": {"user_id": 1, "name": "Alice"},
                    "meta": {"source": "frontend"},
                }
            }
        )

    # Wrong payload shape for UserEvent
    with pytest.raises(ValidationError):
        EventWrapper.model_validate(
            {
                "event": {
                    "kind": "user",
                    "payload": {"user_id": "not-int", "name": "Alice"},
                    "meta": {"source": "frontend"},
                }
            }
        )

    # Wrong meta shape for SystemEvent
    with pytest.raises(ValidationError):
        EventWrapper.model_validate(
            {
                "event": {
                    "kind": "system",
                    "payload": {"message": "down", "code": 503},
                    "meta": {"severity": "not-int"},
                }
            }
        )
