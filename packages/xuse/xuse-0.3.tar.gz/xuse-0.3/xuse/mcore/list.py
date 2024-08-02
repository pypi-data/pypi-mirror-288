"""针对列表（尤其是字典列表）的工具函数"""

from .dtype import Union, Callable, T, K, D
from .dtype import RoList, List, Tuple


def find(items: RoList[T], func: Callable[[T], bool]) -> Union[T, None]:
    for item in items:
        if func(item):
            return item
    return None


def findIndex(items: RoList[T], func: Callable[[T], bool]) -> Union[int, None]:
    for index, item in enumerate(items):
        if func(item):
            return index
    return None


def findWithIndex(items: RoList[T], func: Callable[[T], bool]) -> Union[Tuple[int, T], None]:
    for index, item in enumerate(items):
        if func(item):
            return index, item
    return None


def pick(items: RoList[T], func: Callable[[T], bool]) -> List[T]:
    arr = []
    for item in items:
        if func(item):
            arr.append(item)
    return arr


def omit(items: RoList[T], func: Callable[[T], bool]) -> List[T]:
    arr = []
    for item in items:
        if not func(item):
            arr.append(item)
    return arr


def assign(target: List[T], source: RoList[T], key: Union[D, Callable[[T], K]] = None) -> List[T]:
    if key is None:
        for d in source:
            target.append(d)
    elif isinstance(key, str):
        qs = set([d[key] for d in target])
        for d in source:
            if d[key] not in qs:
                qs.add(d[key])
                target.append(d)
    else:
        qs = set([key(d) for d in target])
        for d in source:
            if key(d) not in qs:
                qs.add(key(d))
                target.append(d)
    return target
