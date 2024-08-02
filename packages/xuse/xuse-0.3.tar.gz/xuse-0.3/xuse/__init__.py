from .core import *
from .mcore import *


def auto_install_dependencies():
    """自动安装 xuse.core 需要的所有依赖包"""
    from more import pip

    pip.install_package("loguru")
