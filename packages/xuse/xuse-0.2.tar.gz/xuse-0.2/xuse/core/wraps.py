import json


__all__ = ["ReturnData"]


class ReturnData(object):
    """Wrap the return code and message."""

    MESSAGE_ELIDED_SIZE = 50

    def __init__(self, code: int, data=None, extra=None) -> None:
        self.code = code
        self.data = data
        self.extra = extra or {}

    def __str__(self) -> str:
        s = self._data_str()
        n = ReturnData.MESSAGE_ELIDED_SIZE
        if len(s) > n:
            s = s[:n] + "..."
        return f"ReturnData({self.code}, {s})"

    def _data_str(self):
        if isinstance(self.data, str):
            return self.data
        try:
            s = json.dumps(self.data)
        except Exception:
            return str(self.data)
        else:
            return s

    @staticmethod
    def set_message_elided_size(n: int):
        """设置打印对象时，对（字符串化的）数据的截取长度，默认为 50"""
        ReturnData.MESSAGE_ELIDED_SIZE = n
