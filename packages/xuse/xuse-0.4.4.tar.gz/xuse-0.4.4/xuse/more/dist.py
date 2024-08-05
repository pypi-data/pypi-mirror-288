import os, re
from typing import Tuple, Sequence
from xuse.mcore._list import sort_recursive

M3Item = Tuple[int, int, int]
M3ItemList = Sequence[M3Item]


def __match_to_m3_versions(m: re.Match[str]):
    a = m.groups()
    if len(a) == 0:
        raise ValueError("No version capture groups")
    major = 0
    minor = 0
    micro = 0
    if len(a) >= 1:
        major = int(a[0])
    if len(a) >= 2:
        minor = int(a[1])
    if len(a) >= 3:
        micro = int(a[2])
    return major, minor, micro


def find_latest_version(target_dir: str, pattern: str = None):
    """
    找到指定目录下的最新版本的打包文件，默认匹配格式形如 xuse-0.2.2.tar.gz
    """
    pattern = pattern or r"\w+-(\d+)\.(\d+)\.tar\.gz"

    items = []
    for fn in os.listdir(target_dir):
        if m := re.match(pattern, fn):
            fp = os.path.join(target_dir, fn)
            vd = __match_to_m3_versions(m)
            item = {"fp": fp, "vd": vd}
            items.append(item)

    sorted_items = sort_recursive(
        items,
        key0=lambda d: d["vd"][0],
        key1=lambda d: d["vd"][1],
        key2=lambda d: d["vd"][2],
        key0_reverse=True,
        key1_reverse=True,
        key2_reverse=True,
    )

    return sorted_items[0]["fp"]
