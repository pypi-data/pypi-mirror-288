import pathlib


def statistic_files_count(src_dir, wildcard="**/*.jpg"):
    """统计文件夹内, 某个类型的文件数量。
    Args:
        src_dir(str): 源文件目录。
        wildcard(str): 通配符。
    Returns:
        返回该目录内的指定类型文件的数量。
    """
    src_dir = pathlib.Path(src_dir)
    src_file_paths = src_dir.glob(wildcard)
    file_count = sum([1 for _ in src_file_paths])
    return file_count
