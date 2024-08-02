import sys
import pathlib


def glob_paths(src_dir, wildcards=["**/*"]):
    """通过通配符, 读取目录下多种后缀名的文件, 比如["**/*.txt", "**/*.jpg"]。
    Args:
        path(str): 文件夹路径。
        wildcards: str list类型。通配符列表, 如["**/*.txt", "**/*.jpg"]。
    Returns:
        paths(pathlib.Path): 返回文件路径list列表。
    """
    paths = []
    src_dir = pathlib.Path(src_dir)
    for w in wildcards:
        paths.extend(src_dir.glob(w))
    return paths


def glob_subdirs(src_dir, parents=False):
    """获取目录下的所有子目录, 返回子目录。
    Args:
        src_dir(str): 文件夹路径。
        parents(bool): True时, 返回的子目录是相对str_dir的相对目录。
    Returns:
        sub_dirs(str list): 即所有子目录名称。
    """
    src_dir = pathlib.Path(src_dir)
    # 获取目录下的所有子目录
    sub_dirs = [x for x in src_dir.glob("*/**") if x.is_dir()]

    # 去除父目录
    if parents:
        # 较新python3.8以上才支持pathlib的relative_to()
        if sys.version_info < (3, 8):
            parent_len = len(src_dir.parts)
            sub_dirs = [pathlib.PurePath(*d.parts[parent_len:]) for d in sub_dirs]
            sud_dirs = [str(d) for d in sub_dirs]
        else:
            sub_dirs = [x.relative_to(src_dir) for x in sub_dirs]

    return sub_dirs


def glob_same_tree(src_dir, dst_dir, wildcard="**/*.jpg", remove=False):
    """保存路径生成器。使用和源目录相同的目录结构, 生成对应的保存目录。
    Args:
        src_dir(str): 源文件夹路径。
        dst_dir(str): 目标文件夹路径。
        wildcard(str): 文件通配符。
        remove(bool): True时, 如果dst_dir目录已经存在, 则删除目录, 重新创建目录。
    Returns:
        返回生成器。生成器产生: (源文件路径, 保存文件路径)。
    """
    src_dir = pathlib.Path(src_dir)
    dst_dir = pathlib.Path(dst_dir)

    # 检测目录是否存在
    if remove and dst_dir.exists():
        shutil.rmtree(dst_dir)
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True)
    for subdir in subdirs:
        subdir = dst_dir / subdir
        if not subdir.exists():
            subdir.mkdir(parents=True)
    
    # 较新python3.8以上才支持pathlib的relative_to()
    if sys.version_info < (3, 8):
        parent_len = len(src_dir.parts)
        for src_path in src_dir.glob(wildcard):
            if src_path.is_dir():
                continue
            dst_path = dst_dir / pathlib.PurePath(*src_path.parts[parent_len:])
            yield src_path, dst_path
    else:
        for src_path in src_dir.glob(wildcard):
            if src_path.is_dir():
                continue
            dst_path = dst_dir / src_path.relative_to(src_dir)
            yield src_path, dst_path
