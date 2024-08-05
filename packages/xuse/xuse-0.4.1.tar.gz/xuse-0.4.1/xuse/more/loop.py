import time
from typing import Callable,NoReturn

def wait(when:Callable[[],bool]=None, sleep=1, timeout=10, callback:Callable[[],NoReturn]=None):
    """
    - `when`: 此条件函数的返回值为真时执行 while 循环
    - `sleep`: 每次循环体执行完成之后睡眠指定秒数
    - `timeout`: 循环执行时间，超过这个秒数会抛出 TimeoutError
    - `callback`: 每次循环体执行的额外功能
    """
    # when
    if when is None:
        when = lambda: True
    if not callable(when):
        raise ValueError("'when' must be a callable object.")
    
    # callback
    if callback is not None and not callable(callback):
        raise ValueError("'callback' must be a callable object.")
    
    start = time.time()
    while when():
        end = time.time()
        if end - start > timeout:
            raise TimeoutError(f"wait_when timeout ({timeout}s)")
        if callback:
            callback()
        if sleep and sleep > 0:
            time.sleep(sleep)