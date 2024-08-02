import pathlib
import shutil


def copy_copytree(src_dir, dst_dir, remove=True):
    """复制目录及其目录中的文件。
    Args:
        src_dir(str): 源目录路径。
        dst_dir(str): 目标目录路径。
        remove(bool): True, 若dst_dir存在则清空原内容; False, 若dst_dir存在则抛出异常。
    """
    if remove:
        shutil.rmtree(dst_dir, ignore_errors=remove)
    shutil.copytree(src_dir, dst_dir)


def copy_dirtree(src_dir, dst_dir, remove=False):
    """复制目录结构, 不复制目录中文件, 即在该路径下创建相关子目录。
    Args:
        src_dir(str): 源文件夹路径。
        dst_dir(str): 目标文件夹路径。
        remove(bool): True, 若dst_dir存在则被清空重建。
    """
    src_dir = pathlib.Path(src_dir)
    # 获取目录下的所有子目录
    sub_dirs = [x for x in src_dir.glob("*/**") if x.is_dir()]
    if sys.version_info < (3, 8):  # python3.8以上才支持pathlib的relative_to()
        parent_len = len(src_dir.parts)
        sub_dirs = [pathlib.PurePath(*d.parts[parent_len:]) for d in sub_dirs]
        sud_dirs = [str(d) for d in sub_dirs]
    else:
        sub_dirs = [x.relative_to(src_dir) for x in sub_dirs]
    # 创建子目录
    if remove and dst_dir.exists():
        shutil.rmtree(dst_dir)
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)
    for sub_dir in sub_dirs:
        sub_dir = dst_dir / sub_dir
        if not sub_dir.exists():
            sub_dir.mkdir(parents=True)
