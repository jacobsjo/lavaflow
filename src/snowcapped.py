from beet import Context
from beet.contrib.worldgen import Dimension
from src.lib.BiomeColors import BiomeColors
from subprocess import DEVNULL, STDOUT, check_call

def beet_default(ctx: Context):
    cache = ctx.cache.get("snowcapped").get_path("the_nether")
    cache.mkdir(parents=True, exist_ok=True)

    dimension_file = cache / "dimension.json"
    biome_colors_file = cache / "biome_colors.json"

    check_call(['npx', 'snowcapped', 'snowcapped.json', '-d', dimension_file, "-c", biome_colors_file], stdout=DEVNULL, stderr=STDOUT)

    ctx.data["minecraft:the_nether"] = Dimension(source_path=dimension_file)
    ctx.data["c:biome_colors"] = BiomeColors(source_path=biome_colors_file)
 