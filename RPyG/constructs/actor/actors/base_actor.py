from dataclasses import dataclass

from RPyG.utilities import ensure_type


@dataclass(frozen=True, slots=True, kw_only=True)
class ActorProperties:
    name: str
    strength: int
    intellect: int
    agility: int
    luck: int

    def __post_init__(self):
        ensure_type(self.name, str, "name")
        ensure_type(self.strength, int, "strength")
        ensure_type(self.intellect, int, "intellect")
        ensure_type(self.agility, int, "agility")
        ensure_type(self.luck, int, "luck")
        if self.name == "":
            raise ValueError("Actor name must be at least 1 characters")


class Actor:
    name: str
    strength: int
    intellect: int
    agility: int
    luck: int
    __slots__: tuple[str, ...] = (
        "name",
        "strength",
        "intellect",
        "agility",
        "luck",
    )

    def __init__(self, properties: ActorProperties) -> None:
        ensure_type(properties, ActorProperties, "properties")

        self.name = properties.name
        self.strength = properties.strength
        self.intellect = properties.intellect
        self.agility = properties.agility
        self.luck = properties.luck
