import json

json_load = json.load
json_loads = json.loads
json_dump = json.dump
json_dumps = json.dumps

__all__ = [
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
