import sys
import subprocess
from os import system
from ..core import logger

__all__ = ["system", "run", "run_quiet"]


def _run_on_linux(command: str, sudo: str = None, local_lang: bool = False) -> str:

    if not local_lang:
        command2 = f"LC_ALL=C {command}"

    command3 = command2
    if sudo is not None:
        if sudo.strip() == "":
            command3 = f"sudo {command2}"
        else:
            command3 = f"echo '{sudo}' | sudo -S -p '' {command2}"

    logger.debug(f"xuse.more.shell.run: {command3}")

    proc = subprocess.run(command3, shell=True, capture_output=True, encoding="utf-8")
    if proc.returncode == 0:
        return proc.stdout.strip()

    logger.exit(proc.stderr, proc.returncode)


def run(command: str, sudo: str = None, local_lang: bool = False):
    """运行命令，运行成功时返回标准输出，运行出错时打印标准错误并直接退出程序"""
    return _run_on_linux(command, sudo=sudo, local_lang=local_lang)


def run_quiet(command: str):
    """运行命令，不显示任何信息，但是运行出错时会直接退出程序"""
    proc = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if proc.returncode != 0:
        sys.exit(proc.returncode)
