"""一些随机工具函数"""

import string
from random import choices

__all__ = ["sk"]


def sk1(length=16):
    """只包含数字和字母的随机字符串"""
    characters = string.ascii_letters + string.digits
    random_chars = "".join(choices(characters, k=length))
    return random_chars
