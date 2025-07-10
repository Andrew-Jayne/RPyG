from utilites.utilities import ensure_type


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

        self.name = name
        self.strength = strength
        self.intellect = intellect
        self.agility = agility
        self.luck = luck


class Party:
    members: list[Actor]

    def __init__(
        self,
        members: list[Actor],
    ) -> None:
        ensure_type(members, list, "members")
        for party_member in members:
            ensure_type(party_member, Actor, "party_member")

        self.members = members

    def lose_member(self, member) -> None:
        self.members.remove(member)

    def gain_member(self, member) -> None:
        self.members.append(member)
