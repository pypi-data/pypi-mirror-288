from typing import Any, Callable, TypeVar

from returns.curry import curry, partial

__all__ = [
    "isinstance_",
    "issubclass_",
    "divmod_",
    "map_",
    "filter_",
    "next_",
]


__ReturnType = TypeVar("__ReturnType")

isinstance_ = curry(isinstance)
issubclass_ = curry(issubclass)
divmod_ = curry(divmod)


@curry
def getattr_(
    o: Any, name: str, default: __ReturnType = None
) -> Callable[[object], __ReturnType | None]:
    return getattr(o, name, default)


def map_(function: Callable):
    return partial(map, function)


def filter_(function: Callable | None):
    return partial(filter, function)


@curry
def next_(default):
    return partial(next, default)
