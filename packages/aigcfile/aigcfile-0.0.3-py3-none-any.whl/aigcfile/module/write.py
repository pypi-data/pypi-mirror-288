from aigcfile.text.write import TextWrite


class Write(object):

    def __init__(self, filetype):
        self.filetype = filetype

    def __call__(self, mode="same", *args, **kwargs):
        if self.filetype == "text":
            writer = TextWrite(mode)
        writer(*args, **kwargs)
