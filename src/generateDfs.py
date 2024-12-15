from beet.contrib.worldgen import Context, WorldgenDensityFunction
import src.density_functions as df

LARGE = 1000000

def beet_default(ctx: Context):
    shift_x = (df.shift_a('lavaflow:shift') * 8).register(ctx, 'lavaflow:shift_x')
    shift_z = (df.shift_b('lavaflow:shift') * 8).register(ctx, 'lavaflow:shift_z')

    ridge = df.shifted_noise('lavaflow:ridge', 1, 0, shift_x, 0, shift_z).cache_2d().register(ctx, 'lavaflow:ridge')
    continentalness = df.shifted_noise('lavaflow:continentalness', 1, 0, shift_x, 0, shift_z).cache_2d().register(ctx, 'lavaflow:continentalness')
    erosion = df.shifted_noise('lavaflow:erosion', 1, 0, shift_x, 0, shift_z).cache_2d().register(ctx, 'lavaflow:erosion')
    temperature = df.noise('lavaflow:temperature', 1, 0).cache_2d().flat_cache().register(ctx, 'lavaflow:temperature')
    humidity = df.noise('lavaflow:humidity', 1, 0).cache_2d().flat_cache().register(ctx, 'lavaflow:humidity')
    depth = df.y_clamped_gradient(-48, 336, 1.5, -1.5).register(ctx, 'lavaflow:depth')

    ridge_abs = ridge.abs().register(ctx, 'lavaflow:ridge_abs')

    height_variation = df.noise('lavaflow:variation', 1, 0).cache_2d().register(ctx, 'lavaflow:height_variation')
    offset = _offset(ctx, ridge_abs, continentalness, erosion).register(ctx, 'lavaflow:offset')

    layer = _layer(depth, ridge_abs, continentalness, erosion).register(ctx, 'lavaflow:layer')
    upper_layer = _upper_layer(depth).register(ctx, 'lavaflow:upper_layer')
    pillar = _pillar(depth, offset, ridge_abs, continentalness, erosion).register(ctx, 'lavaflow:pillar')
    caves = _caves(depth).register(ctx, 'lavaflow:caves')

    ceiling = -depth + (height_variation * 0.095 + 0.12)
    floor = depth + offset + 0.05 * height_variation
    base_terrain = df.min(df.max(ceiling, floor, layer, upper_layer), caves).cache_once().interpolated()
    final_density = (df.max(base_terrain, pillar) - df.beardifier()).register(ctx, 'lavaflow:final_density')

    barrier = df.range_choice(ridge_abs, 0, 0.06, -2, 0.5).register(ctx, 'lavaflow:barrier')
    aquifer = _aquifer(ridge_abs, continentalness, erosion).register(ctx, 'lavaflow:aquifer')

def beardifier_remove(input: df.DensityFunction, negative = -1, positive = -1):
    return df.range_choice(df.beardifier(), -LARGE, -0.01, negative, df.range_choice(df.beardifier(), 0.01, LARGE, positive, input))

def _offset(
    ctx: Context,
    ridge_abs: df.DensityFunction,
    continentalness: df.DensityFunction,
    erosion: df.DensityFunction
):
    offset_beach = df.spline(df.Spline(ridge_abs)
        .add(0.05, -0.93)
        .add(0.07, -0.86)
    ).register(ctx, 'lavaflow:offset/beach')

    offset_valley = df.spline(df.Spline(ridge_abs)
        .add(0.03, -0.92)
        .add(0.1, -0.83)
        .add(0.4, -0.83)
        .add(0.5, -0.5)
    ).register(ctx, 'lavaflow:offset/valley')

    offset_canyon = df.spline(df.Spline(ridge_abs)
        .add(0.05, -0.93)
        .add(0.2, -0.5)
    ).register(ctx, 'lavaflow:offset/canyon')

    offset_plateau = df.spline(df.Spline(ridge_abs)
        .add(0.05, -0.64)
        .add(0.1, -0.5)
    ).register(ctx, 'lavaflow:offset/plateau')

    offset_middle = df.spline(df.Spline(erosion)
        .add(-0.3, offset_valley)
        .add(-0.28, offset_canyon)
        .add(0.2, offset_canyon)
        .add(0.205, offset_plateau)
    ).register(ctx, 'lavaflow:offset/middle')

    return df.spline(df.Spline(continentalness)
        .add(-0.25, -0.95)
        .add(-0.2, offset_beach)
        .add(-0.19, offset_beach)
        .add(-0.16, offset_middle)
    )


def _pillar(
    depth: df.DensityFunction,
    offset: df.DensityFunction,
    ridge_abs: df.DensityFunction,
    continentalness: df.DensityFunction,
    erosion: df.DensityFunction
):
    toggle_river = (df.Spline(ridge_abs)
        .add(0.05, -1)
        .add(0.1, 0)
    )
    toggle_valley = (df.Spline(ridge_abs)
        .add(0.05, -1)
        .add(0.1, -0.2)
        .add(0.35, -0.2)
        .add(0.45, 0)
    )
    toggle = df.spline(df.Spline(continentalness)
        .add(-0.27, 0)
        .add(-0.24, df.Spline(erosion)
            .add(-0.32, toggle_valley)
            .add(-0.28, toggle_river)
        )
    )
    base_thickness = df.spline(df.Spline(depth)
        .add(0.03, -0.15, -0.3)
        .add(0.3, df.Spline(depth+offset)
            .add(-0.2, -0.4)
            .add(0, -0.2))
    )
    thickness = (base_thickness + toggle).cache_2d().interpolated()
    return thickness + df.noise('lavaflow:pillar', 5.0, 0.2)


def _caves(
    depth: df.DensityFunction,
):
    cave_height = df.noise('lavaflow:cave_height', 0.7, 0) * 0.18 - 0.734
    y_density = df.square(cave_height + depth)
    xz_density = df.square(df.noise('lavaflow:cave_ridge', 0.7, 0) * 0.3)
    return (y_density + xz_density - 0.002) * 100


def _layer(
    depth: df.DensityFunction,
    ridge_abs: df.DensityFunction,
    continentalness: df.DensityFunction,
    erosion: df.DensityFunction
):
    toggle_ocean_lavafalls = (df.Spline(erosion)
        .add(0.2, 0)
        .add(0.21, df.Spline(ridge_abs)
            .add(0.1, -1)
            .add(0.12, 0)
        )
    )

    toggle_inland = (df.Spline(erosion)
        .add(0.17, 0)
        .add(0.18, -1)
    )

    toggle_terrain = df.spline(df.Spline(continentalness)
        .add(-0.25, 0)
        .add(-0.24, toggle_ocean_lavafalls)
        .add(-0.12, toggle_ocean_lavafalls)
        .add(-0.1, toggle_inland)
    )

    toggle = beardifier_remove(toggle_terrain, -1, 0)

    layer_height = df.noise('lavaflow:layer_height', 1, 0) * 0.05 - 0.55
    y_density = abs(layer_height + depth)
    xz_density = abs(df.noise('lavaflow:layer_gaps', 1, 0)) * 0.1 - 0.03
    return -(y_density + xz_density) + toggle


def _upper_layer(
    depth: df.DensityFunction,
):
    toggle = beardifier_remove(0)

    layer_height = df.noise('lavaflow:layer_height_upper', 1, 0) * 0.07 - 0.26
    y_density = abs(layer_height + depth)
    xz_density = abs(df.noise('lavaflow:layer_gaps_upper', 1, 0)) * 0.2 - 0.03
    return -(y_density + xz_density) + toggle

def _aquifer(
    ridge_abs: df.DensityFunction,
    continentalness: df.DensityFunction,
    erosion: df.DensityFunction
):
    spline = df.spline(df.Spline(continentalness)
        .add(-0.29, 0.2)
        .add(0.09, df.Spline(erosion)
            .add(0.1, 0.2)
            .add(0.3, df.Spline(ridge_abs)
                .add(0.1, 0.6)
                .add(0.3, 0.2)
            )
        )
    )
    return df.range_choice(df.ref('minecraft:y'), 60, 79, spline, -1)
