import os
import sys
from importlib import import_module

PYTHON_PATH = sys.executable
INDEX_URL = 1

__INDEX_URL_DICT__ = {
    0: "https://pypi.python.org/simple",
    1: "https://pypi.tuna.tsinghua.edu.cn/simple",
}


def is_installed(package: str, version: str = None):

    try:
        module = import_module(package)
    except ImportError:
        return False
    else:
        if hasattr(module, "__version__") and module.__version__ == version:
            return True
        else:
            return False


def install(package: str, version: str = None, validator=None, index_url=None, quiet=False):
    _validator = validator or package
    if isinstance(_validator, str):
        if is_installed(_validator, version=version):
            return -1
    elif callable(_validator):
        if _validator():
            return -1
    else:
        raise ValueError("invalid validator")

    _package = f"{package}=={version}" if version else package
    _index = 1 if index_url is None else index_url
    _index_url = __INDEX_URL_DICT__.get(_index, index_url)
    cmd = f"{PYTHON_PATH} -m pip install {_package} -i {_index_url}"
    if quiet:
        cmd = f"{cmd} >{os.devnull} 2>&1"
    return os.system(cmd)


def remove(package: str, quiet=False):
    cmd = f"{PYTHON_PATH} -m pip uninstall -y {package}"
    if quiet:
        cmd = f"{cmd} >{os.devnull} 2>&1"
    return os.system(cmd)
