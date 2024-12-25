from beet.contrib.worldgen import Context, WorldgenNoiseSettings
from src.lib.surface_rules import *
from src.lib.VerticalAnchor import *

LARGE = 1000000

def beet_default(ctx: Context):
    bedrock_floor = block('minecraft:bedrock').when(gradient('minecraft:bedrock_floor', above_bottom(0), above_bottom(5)))
    bedrock_roof = block('minecraft:bedrock').when(gradient('minecraft:bedrock_roof', below_top(5), below_top(0)).invert())

    soul_sand_valley_selection = block('minecraft:soul_sand').when(noise('minecraft:nether_state_selector', 0, 10000))\
        .otherwise(block('minecraft:soul_soil'))
    nether_wastes_selection = block('minecraft:orange_terracotta').when(noise('minecraft:nether_state_selector', -0.6, -0.25))\
        .otherwise(block('minecraft:red_terracotta').when(noise('minecraft:nether_state_selector', 0.2, 10000)))

    top = soul_sand_valley_selection.when(biome(['minecraft:soul_sand_valley', 'lavaflow:soul_sand_valley_river']))\
        .otherwise(block('minecraft:gravel').when(biome(['lavaflow:gravel_beach'])).when(above_y(absolute(38)).invert()))\
        .otherwise(block('minecraft:crimson_nylium').when(biome(['lavaflow:old_growth_crimson_forest', 'lavaflow:crimson_forest_layer', 'minecraft:crimson_forest']))\
            .otherwise(block('minecraft:warped_nylium').when(biome(['lavaflow:old_growth_warped_forest', 'lavaflow:warped_forest_layer', 'minecraft:warped_forest'])))\
            .when(above_y(absolute(31)))
        )\
        .when(top_block('floor'))

    surface_block = block('minecraft:soul_soil').when(biome(['minecraft:soul_sand_valley', 'lavaflow:soul_sand_valley_river', 'lavaflow:ghost_forest']))\
        .otherwise(nether_wastes_selection.when(biome([ "minecraft:nether_wastes", "lavaflow:nether_wastes_layer", "lavaflow:river"])))\
        .when(is_surface('floor'))

    netherrack_floor = block('minecraft:netherrack').when(is_surface('floor', 20)).when(biome(['lavaflow:caves']).invert())

    floor = top\
        .otherwise(surface_block)\
        .otherwise(netherrack_floor)\
        .when(surface_above_y(below_top(0)).invert())

    ceiling = block('minecraft:smooth_basalt').when(noise('lavaflow:ceiling_stripes', -0.2, 0.2)).when(above_y(absolute(110)))\
        .otherwise(block('minecraft:netherrack'))\
        .when(is_surface('ceiling', 20))\
        .when(biome(['lavaflow:caves']).invert())\
        .when(above_y(above_bottom(20)))

    final_rule = bedrock_floor\
        .otherwise(bedrock_roof)\
        .otherwise(floor)\
        .otherwise(ceiling)

    noise_settings = ctx.data[WorldgenNoiseSettings]['lavaflow:nether']
    noise_settings.data['surface_rule'] = final_rule.generate()
    ctx.data['lavaflow:nether'] = noise_settings