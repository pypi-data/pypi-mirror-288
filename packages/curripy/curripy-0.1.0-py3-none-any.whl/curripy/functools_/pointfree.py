from functools import partialmethod, partial
from typing import Callable, Iterable
from operator import attrgetter

__all__ = []

get_partial_func: Callable[[partial | partialmethod], Callable] = attrgetter("func")
get_partial_args: Callable[[partial | partialmethod], Iterable] = attrgetter("args")
get_partial_keywords: Callable[[partial | partialmethod], Iterable] = attrgetter(
    "keywords"
)
