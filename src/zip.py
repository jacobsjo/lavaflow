from typing import List, Dict
from beet import Context, JsonFile, PluginOptions, configurable, PackExtraContainer
from src.tomlFile import TomlFile
from zipfile import ZipFile
import warnings

class ZipOptions(PluginOptions):
    name: str | None = None


def beet_default(ctx: Context):
    ctx.require(zip)

@configurable(validator=ZipOptions)
def zip(ctx: Context, opts: ZipOptions):
    filename_template = opts.name if opts.name is not None else ('{{project_id}}_{{project_version}}_mod' if ctx.project_version != '' else '{{project_id}}_mod')

    ctx.output_directory.mkdir(parents=True, exist_ok=True)
    with ZipFile(f'{ctx.output_directory}/{ctx.template.render_string(filename_template)}.zip', mode="w") as z:
        ctx.data.dump(z)
        