import pathlib
import cv2
from tqdm import tqdm
from aigcfile.utils.globfile import glob_paths


class ImageRename(object):
    """图片文件修改名称, 特别是修改后缀名后, 一般要重新编码。
    """

    def __init__(self, mode="sequence"):
        self.mode = mode
    
    def stem(self, src_path, dst_path):
        """只是修改文件名, 不修改后缀
        """
        dst_path = dst_path.parent / f"{dst_path.stem}.{src_path.suffix}"
        src_path.rename(dst_path)

    def name(self, src_path, dst_path):
        """修改文件名称, src和dst后缀名称不同时, 重新编码.
        """
        if src_path.suffix == dst_path.suffix:
            src_path.rename(dst_path)
        else:
            image = cv2.imread(str(src_path))
            cv2.imwrite(str(dst_path), image)
            src_path.unlink()

    def sequence(self, src_dir, name="{:0>8d}", suffix=".png", wildcards=[".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"], verbose=True, *args, **kwargs):
        """在当前目录内, 对文件进行重新命名, 名称格式由name指定, 输出格式由suffix指定。
        """
        name = name + "{}"
        wildcards = ["*{}".format(s) for s in wildcards]
        src_dir = pathlib.Path(src_dir)
        sub_dirs = [x for x in src_dir.glob("*/**") if x.is_dir()]
        sub_dirs.append(src_dir)

        for sub_dir in sub_dirs:
            src_paths = sorted(glob_paths(sub_dir, wildcards))
            # if verbose:
            #     src_paths = tqdm(src_paths, desc=str(sub_dir))

            for i, src_path in enumerate(tqdm(src_paths, desc=str(sub_dir))):
                dst_path = src_path.parent / name.format(i, suffix)
                if dst_path.exists():
                    j = src_paths.index(dst_path)
                    src_paths[i], src_paths[j] = src_paths[j], src_paths[i]
                else:
                    self.name(src_path, dst_path)

    def __call__(self, *args, **kwargs):
        if self.mode == "sequence":
            self.sequence(*args, **kwargs)
        else:
            raise Exception("mode '{}' not suport!".format(self.mode))
