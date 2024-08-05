"""针对字典的工具函数"""

from .dtype import Dict, RoDict, RoStrList


def assign(target: Dict, source: RoDict):
    if hasattr(source, "items"):
        for k, v in source.items():
            target[k] = v
    return target


def pick(data: RoDict, keys: RoStrList) -> Dict:
    result = {}
    for k in keys:
        if k in data:
            result[k] = data[k]
    return result


def omit(data: RoDict, keys: RoStrList) -> Dict:
    result = {}
    ks = set(keys)
    for k in data:
        if k not in ks:
            result[k] = data[k]
    return result
