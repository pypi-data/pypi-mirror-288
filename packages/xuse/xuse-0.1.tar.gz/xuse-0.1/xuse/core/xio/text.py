__all__ = ["read_text", "write_text"]


def read_text(src_file: str):
    """读取一个文本文件为字符串"""
    with open(src_file, "r") as f:
        return f.read()


def write_text(text: str, dest_file: str, mode=None):
    """将一个字符串写入文本文件，覆盖模式，支持设置文件权限"""
    with open(dest_file, "w") as f:
        f.write(text)

    if mode:
        from more.shell import run

        run(f"chmod {mode} {dest_file}")
