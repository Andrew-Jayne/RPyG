from RPyG.utilities import ensure_type


class Actor:
    name: str
    strength: int
    intellect: int
    agility: int
    luck: int

    def __init__(
        self,
        name: str,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(strength, int, "strength")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        if name == "":
            raise ValueError("Actor name must be at least 1 characters")

        self.name = name
        self.strength = strength
        self.intellect = intellect
        self.agility = agility
        self.luck = luck
