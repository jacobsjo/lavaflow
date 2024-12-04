from beet import JsonFile, NamespaceFileScope
from typing import ClassVar

class BiomeColors(JsonFile):
    """Class representing a dimension."""

    scope: ClassVar[NamespaceFileScope] = ()
    extension: ClassVar[str] = ".json"
