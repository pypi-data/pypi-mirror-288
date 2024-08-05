import os
import shutil

__all__ = [
    "cpfile",
    "mvfile",
    "rmfile",
    "link_file",
    "softlink_file",
]

cpfile = shutil.copyfile
mvfile = shutil.move
rmfile = os.remove
link_file = os.link
softlink_file = os.symlink
