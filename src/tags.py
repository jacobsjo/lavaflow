from beet.contrib.worldgen import Context, WorldgenBiome, WorldgenBiomeTag

def beet_default(ctx: Context):
    all_biomes = WorldgenBiomeTag()

    for biome in ctx.data[WorldgenBiome]:
        if (biome.split(":")[0] == "lavaflow"):
            all_biomes.add(biome)

    ctx.data["lavaflow:all_biomes"] = all_biomes