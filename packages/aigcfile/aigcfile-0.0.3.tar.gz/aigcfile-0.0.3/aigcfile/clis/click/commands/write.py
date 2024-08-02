import ast
import click
from aigcfile.clis.click.utils.datatype import PythonLiteralOption
from aigcfile.module.write import Write


@click.command('write')
@click.option('--filetype', "-t", default="text", help='要处理的文件类型, 可选值: image')
@click.option('--mode', "-m", default="same", help='重命名模式, 可选值: sequence')
@click.option('--src_dir', "-s", default="data/text", help='输入视频文件或所在文件夹')
@click.option('--string', default="your content description", help='添加的文本内容')
@click.option('--wildcards', "-w", cls=PythonLiteralOption, default="['.txt', '.TXT']", help='哪些源文件将被索引')
def cli(filetype, *args, **kwargs):
    """文件重命名。
    aigcfile write -s tmp/text -t text -m same -w '[".txt", ".TXT"]'
    """
    print("被索引的源文件类型{}: {}".format(filetype, kwargs["wildcards"]))
    writer = Write(filetype)
    writer(*args, **kwargs)
