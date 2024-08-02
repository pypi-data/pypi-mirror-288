import sys
from loguru._logger import Core as _Core
from loguru._logger import Logger as _Logger

__all__ = ["logger"]


class Logger(_Logger):
    def exit(self, msg: str, code=1):
        self.error(msg)
        sys.exit(code)

    def set_simplest_format(self):
        """设置为最简单的日志格式: `[等级] 消息`"""
        self.remove()
        self.add(sink=sys.stdout, format="[{level}] {message}")


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
