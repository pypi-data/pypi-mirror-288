"""Protocols for static duck typing hints"""

from typing import Protocol, Self, SupportsIndex, TypeVar

__all__ = [
    "CanEncode",
    "CanStrip",
    "CanSplit",
    "CanStripGeneric",
    "CanSplitGeneric",
    "CanEncodeGeneric",
]


class CanEncode(Protocol):
    def encode(self, encoding: str, errors: str) -> bytes: ...


class CanStrip(Protocol):
    def strip(self, chars: str | None) -> Self: ...


class CanSplit(Protocol):
    def split(
        self,
        sep: str | None = None,
        maxsplit: SupportsIndex = -1,
    ) -> list[str]: ...


CanStripGeneric = TypeVar("CanStripGeneric", bound=str | CanStrip)
CanSplitGeneric = TypeVar("CanSplitGeneric", bound=str | CanSplit)
CanEncodeGeneric = TypeVar("CanEncodeGeneric", bound=str | CanEncode)
