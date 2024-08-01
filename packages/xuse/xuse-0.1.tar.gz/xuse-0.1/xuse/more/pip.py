import sys
import subprocess
from importlib import import_module

from core import ReturnData
from mcore.dtype import IntOrStr

PYTHON_PATH = sys.executable
INDEX_URL = "tsinghua"


def is_package_installed(package: str):
    try:
        import_module(package)
    except ImportError:
        return False
    else:
        return True


def _install_package(installed: str, imported: str = None, index_url: IntOrStr = None):
    """
    Install the specified package.
    Note that the installation names and import names of some packages are inconsistent.

    Args:
    - `installed`: the name when installing the package.
    - `imported`: the name when importing the package. The default is the same as `installed`.
    - `index_url`: pip index source, the default is Tsinghua source.
    """

    if imported is None:
        imported = installed

    if index_url is None:
        index_url = INDEX_URL

    if index_url in ("tsinghua", 1):
        index_url = "https://pypi.tuna.tsinghua.edu.cn/simple"

    arr = [PYTHON_PATH, "-m", "pip", "install", installed]

    if index_url:
        arr.append("-i")
        arr.append(index_url)

    proc = subprocess.run(arr, capture_output=True, encoding="utf-8")
    if proc.returncode == 0:
        return ReturnData(0, "ok")

    return ReturnData(proc.returncode, proc.stderr)


def install_package(installed: str, imported: str = None, index_url: IntOrStr = None):
    if is_package_installed(imported):
        return ReturnData(-1, "this package is already installed")
    return _install_package(installed, imported=imported, index_url=index_url)
