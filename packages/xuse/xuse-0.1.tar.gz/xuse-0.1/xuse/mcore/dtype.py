from typing import __all__
from typing import *

__all__ = [
    *__all__,
    "StrList",
    "RoStrList",
    "RoDict",
    "RoList",
    "T",
    "K",
    "D",
    "R",
    "S",
    "IntOrStr",
]

StrList = List[str]
RoStrList = Sequence[str]
RoDict = Mapping
RoList = Sequence

T = Any
K = Any
D = Any
R = Any
S = Any

IntOrStr = Union[int, str]
