from ..core import xdir
from ..core import xpath as xp
from .shell import run


def decompress_tar_gz(src_file: str, dest_dir: str, shell=False):
    """解压 .tar.gz 文件到指定目录，支持 shell 和内置两种解压方式"""

    assert src_file.endswith(".tar.gz"), f"{src_file} 不是以 .tar.gz 结尾"
    xdir.mkdir(dest_dir)

    if shell:
        run(f"tar -zxf {src_file} -C {dest_dir}")

    else:
        import tarfile

        with tarfile.open(src_file, "r:gz") as tar:
            tar.extractall(dest_dir)


def decompress_gzip(src_file: str, dest_dir: str, shell=False):
    assert src_file.endswith(".gz"), f"{src_file} 不是以 .gz 结尾"
    xdir.mkdir(dest_dir)

    if shell:
        run(f"cp {src_file} {dest_dir} && cd {dest_dir} && gunzip {xp.basename(src_file)}")

    else:
        import gzip

        dest_file = xp.join(dest_dir, xp.splitext(src_file)[0])
        with gzip.open(src_file, "rb") as fin:
            with open(dest_file, "wb") as fout:
                fout.write(fin.read())


def decompress_zip(src_file: str, dest_dir: str, shell=False):
    assert src_file.endswith(".zip"), f"{src_file} 不是以 .zip 结尾"
    xdir.mkdir(dest_dir)

    if shell:
        run(f"cp {src_file} {dest_dir} && cd {dest_dir} && unzip {xp.basename(src_file)}")
    else:
        raise NotImplementedError()


def decompress_auto(src_file: str, dest_dir: str, shell=False):
    if src_file.endswith(".tar.gz"):
        decompress_tar_gz(src_file, dest_dir, shell=shell)
    elif src_file.endswith(".gz"):
        decompress_gzip(src_file, dest_dir, shell=shell)
    elif src_file.endswith(".zip"):
        decompress_zip(src_file, dest_dir, shell=shell)
    else:
        raise NotImplementedError(f"decompress for {src_file}")
