from classes import typeclass
from typing import IO, Any, TypeVar


@typeclass
def split(instance) -> list:
    ...

@typeclass
def write(instance: Any) -> int:
    ...
    
@typeclass
def open(instance):
    ...