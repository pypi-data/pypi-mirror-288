import os
import sys
from importlib import import_module

PYTHON_PATH = sys.executable


def is_installed(package: str):

    try:
        import_module(package)
    except ImportError:
        return False
    else:
        return True


def install(package: str, validator=None, quiet=False):
    validator = validator or package
    if isinstance(validator, str):
        if is_installed(validator):
            return -1
    elif callable(validator):
        if validator():
            return -1
    else:
        raise ValueError("invalid validator")

    index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    cmd = f"{PYTHON_PATH} -m pip install {package} -i {index_url}"
    if quiet:
        cmd = f"{cmd} >{os.devnull} 2>&1"
    return os.system(cmd)


def remove(package: str, quiet=False):
    cmd = f"{PYTHON_PATH} -m pip uninstall -y {package}"
    if quiet:
        cmd = f"{cmd} >{os.devnull} 2>&1"
    return os.system(cmd)
