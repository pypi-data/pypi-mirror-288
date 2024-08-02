import sys
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger

__all__ = ["logger"]


class Logger(_Logger):

    def exit(self, msg: str, code=1):
        self.error(f"{code} {msg}")
        sys.exit(code)

    def set_style(self, **kwargs):
        self.remove()
        kwargs["sink"] = kwargs.get("sink") or sys.stdout
        self.add(**kwargs)

    def set_style_simplest(self, **kwargs):
        """`[等级] 消息`"""
        kwargs["format"] = "[{level}] {message}"
        self.set_style(**kwargs)


# 从 loguru 抄过来的
logger = Logger(
    core=_Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=[],
    extra={},
)
