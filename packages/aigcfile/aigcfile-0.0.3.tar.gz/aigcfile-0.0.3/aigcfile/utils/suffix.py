import pathlib


def suffix_add_suffix(src_dir, suffix):
    """为没有后缀的文件, 加上指定的后缀名。
    Args
        src_dir: 文件所在的目录路径。
        suffix: 要添加的文件后缀, 比如 ".jpg" 、".png" 等。
    """
    for path in pathlib.Path(src_dir).rglob("*"):
        if path.is_file() and len(str(path.name).split(".")) == 1:
            new_name = path.with_name(str(path.name) + suffix)
            path.rename(new_name)
