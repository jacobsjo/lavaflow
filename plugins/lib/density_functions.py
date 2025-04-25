# Copied from https://github.com/misode/gaia-beet/ and slghtly modified
#
# MIT License
#
# Copyright (c) 2022 Misode
# Copyright (c) 2024 jacobsjo
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__all__ = [
    "DensityFunction",
    "DensityFunctionInput",
    "wrap",
    "Spline",
    "SplinePoint",
    "const",
    "ref",
    "add",
    "mul",
    "min",
    "max",
    "half_negative",
    "quarter_negative",
    "square",
    "cube",
    "squeeze",
    "blend_alpha",
    "blend_offset",
    "blend_density",
    "beardifier",
    "old_blended_noise",
    "end_islands",
    "cache_2d",
    "cache_all_in_cell",
    "cache_once",
    "flat_cache",
    "interpolated",
    "shift",
    "shift_a",
    "shift_b",
    "slide",
    "noise",
    "shifted_noise",
    "weird_scaled_sampler",
    "y_clamped_gradient",
    "range_choice",
    "clamp",
    "spline",
    "terrain_shaper_spline",
    "lerp",
    "map_from_unit",
    "mapped_noise",
]

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, TYPE_CHECKING

from beet import Context
from beet.contrib.worldgen import WorldgenDensityFunction

GeneratedDensityFunction = float | str | Dict[str, Any]

DensityFunctionInput = Any

class DensityFunction:
    def generate(self, ctx: Context) -> GeneratedDensityFunction:
        raise NotImplementedError("Density function generate not implemented")

    def __add__(self, other: DensityFunctionInput):
        return TwoArgumentsDF("add", self, wrap(other))

    def __radd__(self, other: DensityFunctionInput):
        return TwoArgumentsDF("add", wrap(other), self)

    def __neg__(self):
        return self * const(-1)

    def __sub__(self, other: DensityFunctionInput):
        return TwoArgumentsDF("add", self, wrap(-other))

    def __rsub__(self, other: DensityFunctionInput):
        return TwoArgumentsDF("add", wrap(other), -self)

    def __mul__(self, other: DensityFunctionInput):
        return TwoArgumentsDF("mul", self, wrap(other))

    def __rmul__(self, other: DensityFunctionInput):
        return TwoArgumentsDF("mul", wrap(other), self)

    def __pow__(self, exp: Literal[2] | Literal[3]):
        if exp == 2:
            return OneArgumentDF("square", self)
        elif exp == 3:
            return OneArgumentDF("cube", self)

    def __abs__(self):
        return OneArgumentDF("abs", self)

    def clamp(self, min: float, max: float):
        return ClampDF(self, min, max)

    def abs(self):
        return OneArgumentDF("abs", self)

    def cache_2d(self):
        return OneArgumentDF("cache_2d", self)

    def cache_all_in_cell(self):
        return OneArgumentDF("cache_all_in_cell", self)

    def cache_once(self):
        return OneArgumentDF("cache_once", self)

    def flat_cache(self):
        return OneArgumentDF("flat_cache", self)

    def interpolated(self):
        return OneArgumentDF("interpolated", self)


    def register(self, ctx: Context, id: str):
        ctx.data[id] = WorldgenDensityFunction(self.generate(ctx))
        return ref(id)



DensityFunctionInput = float | str | DensityFunction

def wrap(input: DensityFunctionInput) -> DensityFunction:
    if isinstance(input, DensityFunction):
        return input
    elif isinstance(input, (int, float)):
        return ConstantDF(input)
    assert isinstance(input, str)
    return ReferenceDF(input)


def generate_id(ctx: Context, id: str):
    if ":" in id:
        return id
    return f"{ctx.meta['gaia_default_namespace']}:{id}"


@dataclass
class ConstantDF(DensityFunction):
    value: float

    def generate(self, ctx: Context):
        return self.value


def const(value: float):
    return ConstantDF(value)


def ref(id: str):
    return ReferenceDF(id)


def add(*arguments: DensityFunctionInput) -> DensityFunction:
    assert len(arguments) > 0
    result = wrap(arguments[-1])
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("add", wrap(a), result)
    return result


def mul(*arguments: DensityFunctionInput) -> DensityFunction:
    assert len(arguments) > 0
    result = wrap(arguments[-1])
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("mul", wrap(a), result)
    return result


def min(*arguments: DensityFunctionInput) -> DensityFunction:
    assert len(arguments) > 0
    result = wrap(arguments[-1])
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("min", wrap(a), result)
    return result


def max(*arguments: DensityFunctionInput) -> DensityFunction:
    assert len(arguments) > 0
    result = wrap(arguments[-1])
    for a in arguments[-2::-1]:
        result = TwoArgumentsDF("max", wrap(a), result)
    return result


def half_negative(argument: DensityFunctionInput):
    return OneArgumentDF("half_negative", wrap(argument))


def quarter_negative(argument: DensityFunctionInput):
    return OneArgumentDF("quarter_negative", wrap(argument))


def square(argument: DensityFunctionInput):
    return OneArgumentDF("square", wrap(argument))


def cube(argument: DensityFunctionInput):
    return OneArgumentDF("cube", wrap(argument))


def squeeze(argument: DensityFunctionInput):
    return OneArgumentDF("squeeze", wrap(argument))


def blend_alpha():
    return NoArgumentsDF("blend_alpha")


def blend_offset():
    return NoArgumentsDF("blend_offset")


def blend_density(argument: DensityFunctionInput):
    return OneArgumentDF("blend_density", wrap(argument))


def beardifier():
    return NoArgumentsDF("beardifier")


def old_blended_noise():
    return NoArgumentsDF("old_blended_noise")


def end_islands():
    return NoArgumentsDF("end_islands")


def cache_2d(argument: DensityFunctionInput):
    return OneArgumentDF("cache_2d", wrap(argument))


def cache_all_in_cell(argument: DensityFunctionInput):
    return OneArgumentDF("cache_all_in_cell", wrap(argument))


def cache_once(argument: DensityFunctionInput):
    return OneArgumentDF("cache_once", wrap(argument))


def flat_cache(argument: DensityFunctionInput):
    return OneArgumentDF("flat_cache", wrap(argument))


def interpolated(argument: DensityFunctionInput):
    return OneArgumentDF("interpolated", wrap(argument))


def shift(noise: str):
    return ShiftNoiseDF("shift", noise)


def shift_a(noise: str):
    return ShiftNoiseDF("shift_a", noise)


def shift_b(noise: str):
    return ShiftNoiseDF("shift_b", noise)


def slide(argument: DensityFunctionInput):
    return OneArgumentDF("slide", wrap(argument))


def noise(noise: str, xz_scale: float = 1, y_scale: float = 1):
    return NoiseDF(noise, xz_scale, y_scale)


def shifted_noise(
    noise: str,
    xz_scale: float = 1,
    y_scale: float = 1,
    shift_x: DensityFunctionInput = 0,
    shift_y: DensityFunctionInput = 0,
    shift_z: DensityFunctionInput = 0,
):
    return ShiftedNoiseDF(
        noise, xz_scale, y_scale, wrap(shift_x), wrap(shift_y), wrap(shift_z)
    )


def weird_scaled_sampler(
    input: DensityFunctionInput,
    noise: str,
    rarity: Literal["type_1"] | Literal["type_2"],
):
    return WeirdScaledSamplerDF(wrap(input), noise, rarity)


def y_clamped_gradient(from_y: int, to_y: int, from_value: float, to_value: float):
    return YClampedGradientDF(from_y, to_y, from_value, to_value)


def range_choice(
    input: DensityFunctionInput,
    min: float,
    max: float,
    in_range: DensityFunctionInput | None = None,
    out_of_range: DensityFunctionInput | None = None,
):
    return RangeChoiceDF(
        wrap(input),
        min,
        max,
        wrap(input if in_range is None else in_range),
        wrap(input if out_of_range is None else out_of_range),
    )


def clamp(
    input: DensityFunctionInput,
    min: float,
    max: float,
):
    return ClampDF(wrap(input), min, max)


def spline(spline: 'Spline', min: float | None = None, max: float | None = None):
    return SplineDF(spline, min, max)


def terrain_shaper_spline(
    spline: Literal["offset"] | Literal["factor"] | Literal["jaggedness"],
    min: float,
    max: float,
    continentalness: DensityFunctionInput,
    erosion: DensityFunctionInput,
    weirdness: DensityFunctionInput,
):
    return TerrainShaperSplineDF(
        spline, min, max, wrap(continentalness), wrap(erosion), wrap(weirdness)
    )


@dataclass
class ReferenceDF(DensityFunction):
    id: str

    def generate(self, ctx: Context):
        return generate_id(ctx, self.id)

    def register(self, ctx: Context, id: str):
        raise TypeError("Can't register reference density function")


@dataclass
class NoArgumentsDF(DensityFunction):
    type: str

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
        )


@dataclass
class OneArgumentDF(DensityFunction):
    type: str
    argument: DensityFunction

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
            argument=self.argument.generate(ctx),
        )


@dataclass
class TwoArgumentsDF(DensityFunction):
    type: str
    argument1: DensityFunction
    argument2: DensityFunction

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
            argument1=self.argument1.generate(ctx),
            argument2=self.argument2.generate(ctx),
        )


@dataclass
class ShiftNoiseDF(DensityFunction):
    type: str
    noise_parameters: str

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:{self.type}",
            argument=generate_id(ctx, self.noise_parameters),
        )


@dataclass
class NoiseDF(DensityFunction):
    noise_parameters: str
    xz_scale: float
    y_scale: float

    def generate(self, ctx: Context) -> Dict[str, Any]:
        return dict(
            type=f"minecraft:noise",
            noise=generate_id(ctx, self.noise_parameters),
            xz_scale=self.xz_scale,
            y_scale=self.y_scale,
        )


@dataclass
class ShiftedNoiseDF(NoiseDF):
    shift_x: DensityFunction
    shift_y: DensityFunction
    shift_z: DensityFunction

    def generate(self, ctx: Context):
        return dict(
            super().generate(ctx),
            type=f"minecraft:shifted_noise",
            shift_x=self.shift_x.generate(ctx),
            shift_y=self.shift_y.generate(ctx),
            shift_z=self.shift_z.generate(ctx),
        )


@dataclass
class WeirdScaledSamplerDF(DensityFunction):
    input: DensityFunction
    noise_parameters: str
    type: Literal["type_1"] | Literal["type_2"]

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:weird_scaled_sampler",
            input=self.input.generate(ctx),
            noise=generate_id(ctx, self.noise_parameters),
            rarity_value_mapper=self.type,
        )


@dataclass
class YClampedGradientDF(DensityFunction):
    from_y: int
    to_y: int
    from_value: float
    to_value: float

    def __post_init__(self):
        assert -4064 <= self.from_y <= 4062
        assert -4064 <= self.to_y <= 4062
        assert -1000000 <= self.from_value <= 1000000
        assert -1000000 <= self.to_value <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:y_clamped_gradient",
            from_y=self.from_y,
            to_y=self.to_y,
            from_value=self.from_value,
            to_value=self.to_value,
        )


@dataclass
class RangeChoiceDF(DensityFunction):
    input: DensityFunction
    min: float
    max: float
    in_range: DensityFunction
    out_of_range: DensityFunction

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:range_choice",
            input=self.input.generate(ctx),
            min_inclusive=self.min,
            max_exclusive=self.max,
            when_in_range=self.in_range.generate(ctx),
            when_out_of_range=self.out_of_range.generate(ctx),
        )


@dataclass
class ClampDF(DensityFunction):
    input: DensityFunction
    min: float
    max: float

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        return dict(
            type=f"minecraft:clamp",
            input=self.input.generate(ctx),
            min=self.min,
            max=self.max,
        )


@dataclass
class Spline:
    coordinate: DensityFunction
    points: List['SplinePoint'] = field(default_factory=lambda: [])

    def generate(self, ctx: Context) -> GeneratedDensityFunction:
        assert len(self.points) > 0

        return dict(
            coordinate=self.coordinate.generate(ctx),
            points=[p.generate(ctx) for p in self.points],
        )

    def add(self, location: float, value: 'float | Spline | DensityFunction', derivative: float = 0):
        if isinstance(value, DensityFunction):
            value = Spline(value).add(0, 0, 1)

        self.points.append(SplinePoint(location, value, derivative))
        return self


@dataclass
class SplinePoint:
    location: float
    value: float | Spline
    derivative: float = 0

    def generate(self, ctx: Context):
        if type(self.value) in (float, int):
            value = self.value
        elif isinstance(self.value, Spline):
            value = self.value.generate(ctx)
        else:
            raise ValueError(f"Invalid cubic spline point value {self.value}")
        return dict(
            location=self.location,
            value=value,
            derivative=self.derivative,
        )


@dataclass
class SplineDF(DensityFunction):
    spline: Spline
    min: float | None
    max: float | None

    def __post_init__(self):
        assert self.min is None or -1000000 <= self.min <= 1000000
        assert self.max is None or -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        if ctx.data.pack_format >= 10:
            return dict(
                type=f"minecraft:spline",
                spline=self.spline.generate(ctx),
            )
        else:
            assert (
                self.min is not None and self.max is not None
            ), f"spline min and max need to be defined for pack format {ctx.data.pack_format}"
            return dict(
                type=f"minecraft:spline",
                spline=self.spline.generate(ctx),
                min=self.min,
                max=self.max,
            )


@dataclass
class TerrainShaperSplineDF(DensityFunction):
    spline: Literal["offset"] | Literal["factor"] | Literal["jaggedness"]
    min: float
    max: float
    continentalness: DensityFunction
    erosion: DensityFunction
    weirdness: DensityFunction

    def __post_init__(self):
        assert -1000000 <= self.min <= 1000000
        assert -1000000 <= self.max <= 1000000

    def generate(self, ctx: Context):
        assert ctx.data.pack_format < 10
        return dict(
            type=f"minecraft:terrain_shaper_spline",
            spline=self.spline,
            min_value=self.min,
            max_value=self.max,
            continentalness=self.continentalness.generate(ctx),
            erosion=self.erosion.generate(ctx),
            weirdness=self.weirdness.generate(ctx),
        )


def lerp(
    a: DensityFunctionInput, b: DensityFunctionInput, c: DensityFunctionInput
) -> DensityFunction:
    neg_a = const(1) + const(-1) * cache_once(a)
    return (wrap(b) * neg_a) + (wrap(c) * cache_once(a))


def map_from_unit(
    input: DensityFunctionInput, min: float, max: float
) -> DensityFunction:
    avg = const((min + max) * 0.5)
    half_diff = const((max - min) * 0.5)
    return avg + half_diff * input


def mapped_noise(
    noise: str, min: float, max: float, xz_scale: float = 1, y_scale: float = 1
) -> DensityFunction:
    return map_from_unit(NoiseDF(noise, xz_scale, y_scale), min, max)
