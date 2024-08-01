from operator import call
from typing import Callable

from ..functionalize_tools import curry_right

__all__ = [
    "pass_arg",
]

pass_arg: Callable[..., Callable] = curry_right(call, arity=2)
