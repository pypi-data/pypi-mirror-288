from operator import methodcaller as m
from typing import Callable, LiteralString, SupportsIndex, TypeVar

from .protocols import CanEncode, CanSplitGeneric, CanStripGeneric

__all__ = ["encode", "split"]


def encode(
    encoding: str = "utf-8", errors: str = "strict"
) -> Callable[[CanEncode], bytes]:
    return m("encode", encoding, errors)


def split(
    sep: str, maxsplit: SupportsIndex = -1
) -> Callable[[CanSplitGeneric], CanSplitGeneric]:
    return m("split", sep, maxsplit)


def strip(
    chars: str | LiteralString | None = None,
) -> Callable[[CanStripGeneric], CanStripGeneric]:
    return m("strip", chars)
