import shutil
from aigcfile.image.rename import *


################################################################################
# ImageRename()
################################################################################
print("\nImageRename(): ")
data_dir = "data/images"
src_dir = "tmp/images"
if pathlib.Path(src_dir).exists():
    shutil.rmtree(src_dir)
shutil.copytree(data_dir, src_dir)

rename = ImageRename(mode="sequence")
rename(src_dir, suffix=".jpg", verbose=True)
