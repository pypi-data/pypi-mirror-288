import ast
import click


class PythonLiteralOption(click.Option):
    """用于click输入list"""

    def type_cast_value(self, ctx, value):
        try:
            return ast.literal_eval(value)
        except:
            raise click.BadParameter(value)
