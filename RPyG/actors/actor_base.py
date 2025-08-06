from typing import Generic, TypeVar

from RPyG.utilites import ensure_type


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


ActorType = TypeVar("ActorType", bound=Actor)


class Party(Generic[ActorType]):
    members: list[ActorType]

    def __init__(
        self,
        members: list[ActorType],
    ) -> None:
        ensure_type(members, list, "members")
        for member in members:
            ensure_type(member, Actor, "member")

        self.members = members

    def lose_member(self, member: ActorType) -> None:
        self.members.remove(member)

    def gain_member(self, member: ActorType) -> None:
        self.members.append(member)
