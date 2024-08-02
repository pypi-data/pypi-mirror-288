from aigcfile.image.rename import ImageRename


class Rename(object):

    def __init__(self, filetype):
        self.filetype = filetype

    def __call__(self, mode="sequence", *args, **kwargs):
        if self.filetype == "image":
            rename = ImageRename(mode)
        rename(*args, **kwargs)
