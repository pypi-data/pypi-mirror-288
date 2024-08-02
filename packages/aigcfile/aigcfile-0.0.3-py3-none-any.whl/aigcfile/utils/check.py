import pathlib
import shutil


def check_dir_exists(src_dir, subdirs=list([]), remove=False):
    """检查文件夹是否存在。
    Args:
        src_dir(str): 要检查的文件夹目录。
        subdirs(string list): 子目录的列表。
        remove(bool): True时, 如果文件夹存在, 则清空文件夹。
    """
    src_dir = pathlib.Path(src_dir)

    if remove and src_dir.exists():
        shutil.rmtree(src_dir)
    if not src_dir.exists():
        src_dir.mkdir(parents=True)

    for subdir in subdirs:
        subdir = src_dir / subdir
        if not subdir.exists():
            subdir.mkdir(parents=True)


def check_is_file(src, dst, remove=False):
    """检查src输入时文件还是目录, 是文件返回True。
    Args:
        src(str), 源文件路径。
        dst(str), 目标文件路径。
        remove(bool), 是否删除源文件。
    """
    src = pathlib.Path(src)
    dst = pathlib.Path(dst)
    if src.is_file():
        if src == dst:
            return True
        if remove and dst.exists():
            dst.unlink()
        if not dst.parent.exists():
            dst.parent.mkdir(parents=True)
        return True
    else:
        if src == dst:
            return False
        if remove and dst.exists():
            shutil.rmtree(dst)
        if not dst.exists():
            dst.mkdir(parents=True)
        return False
