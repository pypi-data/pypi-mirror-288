import shutil
from aigcfile.text.write import *


################################################################################
# TextWrite()
################################################################################
print("\nTextWrite(): ")
data_dir = "data/text"
src_dir = "tmp/text"
if pathlib.Path(src_dir).exists():
    shutil.rmtree(src_dir)
shutil.copytree(data_dir, src_dir)

text_writer = TextWrite(mode="same")
text_writer(src_dir)
