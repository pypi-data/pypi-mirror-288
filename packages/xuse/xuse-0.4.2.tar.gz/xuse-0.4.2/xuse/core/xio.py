import json

json_load = json.load
json_loads = json.loads
json_dump = json.dump
json_dumps = json.dumps

__all__ = [
    "read_text",
    "write_text",
    "read_json",
    "write_json",
    "json_dump",
    "json_dumps",
    "json_load",
    "json_loads",
]


def read_json(src_file: str):
    with open(src_file, "r") as f:
        return json.load(f)


def write_json(data, dest_file: str, indent=2):
    with open(dest_file, "w") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def read_text(src_file: str):
    """读取一个文本文件为字符串"""
    with open(src_file, "r") as f:
        return f.read()


def write_text(text: str, dest_file: str, mode=None):
    """将一个字符串写入文本文件，覆盖模式，支持设置文件权限"""
    with open(dest_file, "w") as f:
        f.write(text)

    if mode:
        from xuse.more.shell import run

        run(f"chmod {mode} {dest_file}")
