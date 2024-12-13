import toml
from typing import Dict, Any, TypeVar, ClassVar
from beet import DataModelBase, FileDeserialize
from dataclasses import dataclass

JsonDict = Dict[str, Any]
ValueType = TypeVar("ValueType", bound=Any)

class TomlFileBase(DataModelBase[ValueType]):
    """Base class for json files."""

    def __post_init__(self):
        super().__post_init__()
        if not self.encoder:  # type: ignore
            self.encoder = toml.dumps
        if not self.decoder:  # type: ignore
            self.decoder = toml.loads


@dataclass(eq=False, repr=False)
class TomlFile(TomlFileBase[JsonDict]):
    """Class representing a toml file."""

    data: ClassVar[FileDeserialize[JsonDict]] = FileDeserialize()

    @classmethod
    def default(cls) -> JsonDict:
        return {}