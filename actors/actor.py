from utilites.utilities import ensure_type


class Actor:
    def __init__(
        self, name: str, strength: int, intellect: int, agility: int, luck: int
    ):
        ensure_type(name, str, "name")
        ensure_type(strength, int, "strengh")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")

        self.name = name
        self.strength = strength
        self.intellect = intellect
        self.agility = agility
        self.luck = luck
