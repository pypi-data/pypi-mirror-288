from os.path import *
from os.path import __all__
from .log import logger


__all__ = [
    *__all__,
    "not_exists",
    "exit_if_exists",
    "exit_if_not_exists",
]


def not_exists(path: str):
    return not exists(path)


def exit_if_exists(_path: str, msg: str = None):
    """如果路径存在，打印错误日志，退出程序"""
    if exists(_path):
        logger.exit(msg or f"Path exists: {_path}")
    return _path


def exit_if_not_exists(_path: str, msg: str = None):
    """如果路径不存在，打印错误日志，退出程序"""
    if not exists(_path):
        logger.exit(msg or f"Path not exists: {_path}")
    return _path
