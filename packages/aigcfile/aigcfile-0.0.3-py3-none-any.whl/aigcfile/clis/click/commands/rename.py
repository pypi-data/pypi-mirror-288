import ast
import click
from aigcfile.clis.click.utils.datatype import PythonLiteralOption
from aigcfile.module.rename import Rename


@click.command('rename')
@click.option('--filetype', "-t", default="image", help='要处理的文件类型, 可选值: image')
@click.option('--mode', "-m", default="sequence", help='重命名模式, 可选值: sequence')
@click.option('--src_dir', "-s", default="data/images", help='输入视频文件或所在文件夹')
@click.option('--dst_dir', "-d", default="", help='输出视频文件或所在文件夹')
@click.option('--suffix', default=".png", help='输出文件后缀名')
@click.option('--wildcards', "-w", cls=PythonLiteralOption, default="['.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG']", help='哪些源文件将被索引')
@click.option('--verbose', default=True, help='是否显示tqdm进度条')
@click.option('--name', default="{:0>8d}", help='输出文件命名格式')
@click.option('--remove', default=False, help='清空dst指向的目录或文件')

def cli(filetype, *args, **kwargs):
    """文件重命名。
    aigcfile rename -s tmp/images -t image -m sequence -w '[".png", ".PNG", ".jpg", ".JPG", ".jpeg", ".JPEG"]'
    """
    print("被索引的源文件类型{}: {}".format(filetype, kwargs["wildcards"]))
    rename = Rename(filetype)
    rename(*args, **kwargs)
