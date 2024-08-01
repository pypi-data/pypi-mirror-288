from functools import partialmethod, partial, reduce as reduce_
from typing import Callable, Iterable
from operator import attrgetter
from returns.curry import curry

__all__ = ["reduce"]


@curry
def reduce(function: Callable, sequence: Iterable):
    return reduce_(function, sequence)
