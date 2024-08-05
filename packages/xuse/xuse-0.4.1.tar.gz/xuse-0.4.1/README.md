安装此包：`pip install xuse`

导入此包：`import xuse as x`


# 用法

## core

core 包下的可以直接通过 `x.` 调用。

### path

包括但不限于 `os.path` 的所有导出

- `x.not_exists()`
- `x.exit_if_exists()`
- `x.exit_if_not_exists()`

### logger

使用 loguru 作为日志模块

```python
from xuse import logger
```

- `logger.exit()`: 打印错误日志，并退出程序
- `logger.set_simplest_format()`: 设置为最简单的日志格式: `[等级] 消息`

### io

简单文本文件的读写。

- `x.read_text()`
- `x.write_text()`
- `x.read_json()`
- `x.write_json()`
- `x.json_dump()`
- `x.json_dumps()`
- `x.json_load()`
- `x.json_loads()`

### file

文件操作。

- `x.cpfile()`
- `x.mvfile()`
- `x.rmfile()`
- `x.link_file()`
- `x.softlink_file()`

目录操作。

- `x.walk()`
- `x.listdir()`
- `x.rmdir()`
- `x.mkdir()`
- `x.mvdir()`
- `x.cpdir()`
- `x.softlink_dir()`

## mcore

mcore 包下的模块作为整体被调用：

- `x.di`: 字典工具
- `x.li`: 列表工具（字典列表）
- `x.dt`: 类型工具，包括但不限于 typing 模块的所有导出
- `x.rd`: 随机数工具

## more

more 包下的模块需要单独导入。

### pip

```python
from xuse.more import pip
```

- `pip.is_package_installed()`
- `pip.install_package()`

### shell

- `shell.system()`
- `shell.run()`
- `shell.run_quiet()`

### interactive

- `get_input()`
- `get_input_zh()`

### docker

- `list_local_docker_images()`

### zipfile

- `decompress_tar_gz()`
- `decompress_gzip()`
- `decompress_zip()`
- `decompress_auto()`
