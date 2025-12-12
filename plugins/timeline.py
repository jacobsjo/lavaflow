__all__ = [
    "timeline",
    "Timeline",
    "TimelineTag"
]


from typing import ClassVar, Union

from beet import Context, DataPack, JsonFile, TagFile, NamespaceFileScope

def beet_default(ctx: Context):
    ctx.require(timeline)

def timeline(pack: Union[Context, DataPack]):
    """Enable timeline."""
    if isinstance(pack, Context):
        pack = pack.data
    pack.extend_namespace += [
        Timeline,
        TimelineTag
    ]


class Timeline(JsonFile):
    """Class representing a dimension."""

    scope: ClassVar[NamespaceFileScope] = ("timeline",)
    extension: ClassVar[str] = ".json"

class TimelineTag(TagFile):
    """Class representing a biome tag."""

    scope: ClassVar[NamespaceFileScope] = ("tags", "timeline")
