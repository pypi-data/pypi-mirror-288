from operator import methodcaller as m
from typing import Any, Callable
from collections import Counter

__all__ = []


def most_common(n: int | None = None) -> Callable[[Counter], list[tuple[Any, Any]]]:
    return m("most_common", n)
