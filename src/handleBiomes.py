from beet import Advancement
from beet.contrib.worldgen import Context, WorldgenBiome, WorldgenBiomeTag
from beet.contrib.vanilla import load_vanilla

def beet_default(ctx: Context):
    allBiomesTag = WorldgenBiomeTag()
    ctx.require(load_vanilla(
        match={
            "advancement": ["minecraft:nether/explore_nether"]
        }
    ))

    exploreNetherAdvancement = ctx.data.advancements['minecraft:nether/explore_nether']

    for biome in ctx.data[WorldgenBiome]:
        if (biome.split(":")[0] == "lavaflow"):
            allBiomesTag.add(biome)
            exploreNetherAdvancement.data['criteria'][biome] = {
                "conditions": {
                    "player": [
                    {
                        "condition": "minecraft:entity_properties",
                        "entity": "this",
                        "predicate": {
                        "location": {
                            "biomes": biome
                        }
                        }
                    }
                    ]
                },
                "trigger": "minecraft:location"
            }
            exploreNetherAdvancement.data['requirements'].append([
                biome
            ])

    ctx.data["lavaflow:all_biomes"] = allBiomesTag
