"""针对列表（尤其是字典列表）的工具函数"""

from collections import defaultdict, OrderedDict
from .dtype import RoList, List, Tuple, Union, Callable, T, K, D


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


KeyFunc_T = Callable[[T], int]


def __sort_recursive__iterator(seqs: RoList[T], key_functions: RoList[KeyFunc_T], key_reverses: RoList[Union[bool, None]]):
    # 没有传入 key 函数时结束递归，直接返回传入的数组
    if len(key_functions) == 0:
        return seqs
    # 取第一个排序函数进行本轮排序，其余排序函数
    active_key_func = key_functions[0]
    active_key_reverse = key_reverses[0]
    if len(key_functions) == 1:
        left_key_functions = []
        left_key_reverses = []
    else:
        left_key_functions = key_functions[1:]
        left_key_reverses = key_reverses[1:]

    ddt = defaultdict(list)
    for o in seqs:
        ddt[active_key_func(o)].append(o)
    odd = {k: ddt[k] for k in sorted(ddt.keys(), reverse=active_key_reverse)}

    sorted_seqs = []
    for sub_seqs in OrderedDict(odd).values():
        sorted_sub_seqs = __sort_recursive__iterator(sub_seqs, left_key_functions, left_key_reverses)
        assign(sorted_seqs, sorted_sub_seqs)

    return sorted_seqs


def sort_recursive(source: RoList[T], **kwargs) -> RoList[T]:
    """
    对数组进行递归排序。排序函数的格式可以是：
    - `key=...`: 优先级最高的排序函数
    - `keyN=...`: 其中 N 是任意自然数，根据 N 的值从小达到进行递归排序
    - `keyN_reverse: bool` 可以设置逆序
    """
    key_functions = {}
    key_reverse = {}
    for k in kwargs.keys():
        if k.startswith("key"):
            if k.endswith("_reverse"):
                s = k.split("_reverse")[0]
                key_reverse[s] = kwargs[k]
            else:
                try:
                    int(k[3:])
                except ValueError:
                    pass
                else:
                    key_functions[k] = kwargs[k]

    if not key_functions:
        raise ValueError("No valid key function provided")

    sorted_keys = sorted(key_functions.keys(), key=lambda s: int(s[3:] or "-1"))
    sorted_key_functions = [key_functions[k] for k in sorted_keys]
    key_reverse_list = [key_reverse.get(k, False) for k in sorted_keys]
    return __sort_recursive__iterator(source, sorted_key_functions, key_reverse_list)
