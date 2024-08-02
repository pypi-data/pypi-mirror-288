import os
import shutil
from os import listdir, walk
from ..mcore.dtype import RoStrList
from . import xpath as xp

__all__ = [
    "walk",
    "listdir",
    "rmdir",
    "mkdir",
    "mvdir",
    "cpdir",
    "softlink_dir",
]


def rmdir(*dps: RoStrList) -> None:
    """目录存在时递归删除目录, 不存在时忽略"""
    dp = xp.join(*dps)
    if not xp.isdir(dp):
        raise NotADirectoryError(dp)
    if xp.exists(dp):
        shutil.rmtree(dp)


def mkdir(*dps: RoStrList) -> str:
    """目录不存在时直接递归创建目录，否则忽略"""
    dp = xp.join(*dps)
    if xp.not_exists(dp):
        os.makedirs(dp)
    elif not xp.isdir(dp):
        raise NotADirectoryError(dp)
    return dp


mvdir = shutil.move
cpdir = shutil.copytree
softlink_dir = os.symlink
