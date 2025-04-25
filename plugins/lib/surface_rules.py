from typing import Dict, List, TypedDict, Any, Literal
from dataclasses import dataclass, field
from plugins.lib.VerticalAnchor import VerticalAnchor

__all__ = [
    'SurfaceRule',
    'block',
    'bandlands',
    'biome',
    'hole',
    'steep',
    'temperature',
    'noise',
    'gradient',
    'top_block',
    'is_surface',
    'above_y',
    'surface_above_y'
]

SurfaceCondition = Any

class SurfaceCondition:
    def generate(self) -> Dict[str, Any]:
        raise NotImplementedError("Surface condition generate not implemented")
    
    def invert(self) -> SurfaceCondition:
        return NotSC(self)

SurfaceRule = Any

class SurfaceRule:
    def generate(self) -> Dict[str, Any]:
        raise NotImplementedError("Surface rule generate not implemented")

    def when(self, condition: SurfaceCondition):
        return ConditionSR(condition, self)

    def otherwise(self, rule: SurfaceRule):
        return SequenceSR([self, rule])

def block(block: Dict[str, Any] | str):
    if isinstance(block, str):
        return BlockSR(dict(Name=block))
        
    return BlockSR(block)

def bandlands():
    return BandlandsSR()

@dataclass
class BlockSR(SurfaceRule):
    result_state: Dict[str, Any]

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:block',
            result_state=self.result_state
        )

@dataclass
class BandlandsSR(SurfaceRule):
    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:bandlands'
        )

@dataclass
class ConditionSR(SurfaceRule):
    if_true: SurfaceCondition
    then_run: SurfaceRule

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:condition',
            if_true=self.if_true.generate(),
            then_run=self.then_run.generate()
        )

@dataclass
class SequenceSR(SurfaceRule):
    sequence: List[SurfaceRule]

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:sequence',
            sequence=list(map(lambda rule: rule.generate(), self.sequence))
        )

    def otherwise(self, rule: SurfaceRule):
        return SequenceSR(self.sequence + [rule])



def biome(biomes: List[str]):
    return BiomeSC(biomes)

def hole():
    return NoParamsSC('biome')

def steep():
    return NoParamsSC('steep')

def temperature():
    return NoParamsSC('temperature')

def noise(noise: str, min: float, max: float):
    return NoiseThresholdSC(noise, min, max)

def gradient(random: str, min: int, max: int):
    return VerticalGradientSC(random, min, max)

def top_block(surface: Literal['ceiling'] | Literal['floor'], offset: int = 0):
    return StoneDepthSC(offset, False, 0, surface)

def is_surface(surface: Literal['ceiling'] | Literal['floor'], secondary: int = 0, offset: int = 0):
    return StoneDepthSC(offset, True, secondary, surface)

def above_y(anchor: VerticalAnchor):
    return YAboveSC(anchor, 0, False)

def surface_above_y(anchor: VerticalAnchor):
    return YAboveSC(anchor, 0, True)

@dataclass 
class BiomeSC(SurfaceCondition):
    biomes: List[str]
    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:biome',
            biome_is=self.biomes
        )

@dataclass 
class NoParamsSC(SurfaceCondition):
    type: str

    def generate(self) -> Dict[str, Any]:
        return dict(
            type=f'minecraft:{self.type}'
        )

@dataclass 
class NoiseThresholdSC(SurfaceCondition):
    noise: str
    min: float
    max: float

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:noise_threshold',
            noise=self.noise,
            min_threshold=self.min,
            max_threshold=self.max
        )

@dataclass 
class NotSC(SurfaceCondition):
    input: SurfaceCondition

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:not',
            invert=self.input.generate()
        )

@dataclass
class StoneDepthSC(SurfaceCondition):
    offset: int
    add_surface_depth: bool
    secondary_depth_range: int
    surface_type: Literal['ceiling'] | Literal['floor']

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:stone_depth',
            offset=self.offset,
            add_surface_depth=self.add_surface_depth,
            secondary_depth_range=self.secondary_depth_range,
            surface_type=self.surface_type
        )

@dataclass
class WaterSC(SurfaceCondition):
    offset: int
    surface_depth_multiplier: int
    add_stone_depth: bool

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:water',
            offset=self.offset,
            surface_depth_multiplier=self.surface_depth_multiplier,
            add_stone_depth=self.add_stone_depth
        )

@dataclass
class YAboveSC(SurfaceCondition):
    anchor: VerticalAnchor
    surface_depth_multiplier: int
    add_stone_depth: bool

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:y_above',
            anchor=self.anchor,
            surface_depth_multiplier=self.surface_depth_multiplier,
            add_stone_depth=self.add_stone_depth
        )

@dataclass
class VerticalGradientSC(SurfaceCondition):
    random_name: str
    min: int
    max: int

    def generate(self) -> Dict[str, Any]:
        return dict(
            type='minecraft:vertical_gradient',
            random_name=self.random_name,
            true_at_and_below=self.min,
            false_at_and_above=self.max
        )