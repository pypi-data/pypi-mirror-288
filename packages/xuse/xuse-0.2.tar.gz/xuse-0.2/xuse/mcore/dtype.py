from typing import *


T = Any
K = Any
D = Any
R = Any
S = Any

IntOrStr = Union[int, str]

RoList = Sequence
StrList = List[str]
IntList = List[int]
RoStrList = Sequence[str]
RoIntList = RoList[int]

RoDict = Mapping
SADict = Dict[str, Any]
SSDict = Dict[str, str]
SBDict = Dict[str, bool]
SIDict = Dict[str, int]
RoSADict = RoDict[str, Any]
RoSSDict = RoDict[str, str]
RoSBDict = RoDict[str, bool]
RoSIDict = RoDict[str, int]
