from dataclasses import dataclass, field
from typing import Generic, TypeVar, override

from RPyG.constructs.actor.actors import (
    Actor,
    CombatantActor,
    EnemyActor,
    PlayableActor,
)
from RPyG.utilities import ensure_type


ActorType = TypeVar("ActorType", bound=Actor)
CombatantType = TypeVar("CombatantType", bound=CombatantActor)


@dataclass(kw_only=True, slots=True)
class ActorParty(Generic[ActorType]):
    members: list[ActorType]

    def __init__(
        self,
        members: list[ActorType],
    ) -> None:
        self.members = members

    def lose_member(self, member: ActorType) -> None:
        self.members.remove(member)

    def gain_member(self, member: ActorType) -> None:
        self.members.append(member)

    def __post_init__(self):
        ensure_type(self.members, list, "members")
        for member in self.members:
            ensure_type(member, Actor, "member")


@dataclass(kw_only=True, slots=True)
class CombatantParty(ActorParty[CombatantType], Generic[CombatantType]):
    name: str
    members: list[CombatantType]
    dead_members: list[CombatantType] = field(default_factory=list)

    @classmethod
    def build(
        cls, name: str, members: list[CombatantType]
    ) -> CombatantParty[CombatantType]:
        return CombatantParty[CombatantType](
            name=name,
            members=members,
        )

    @override
    def lose_member(self, member: CombatantType) -> None:
        from RPyG.core_io import CoreIO, output_models

        core_io = CoreIO.get_core_io()
        core_io.send_output(output_models.ActorDefeatedMessage(actor_name=member.name))
        self.dead_members.append(member)
        self.members.remove(member)

    @override
    def gain_member(self, member: CombatantType) -> None:
        self.members.append(member)

    def __post_init__(self):
        ensure_type(self.name, str, "name")
        ensure_type(self.members, list, "members")
        for party_member in self.members:
            ensure_type(party_member, CombatantActor, "party_member")
        for party_member in self.dead_members:
            ensure_type(party_member, CombatantActor, "party_member")

        if len(self.name) > 64:
            raise ValueError(
                "Combatant Party name may not be longer than 64 characters"
            )
        # Super Because of Generics Gymnastics
        super().__post_init__()


@dataclass(kw_only=True, slots=True)
class EnemyParty(CombatantParty[EnemyActor]):
    members: list[EnemyActor]
    dead_members: list[EnemyActor] = field(default_factory=list)
    loot: object | None = None

    def __post_init__(self):
        ensure_type(self.name, str, "name")
        ensure_type(self.members, list, "members")
        for party_member in self.members:
            ensure_type(party_member, EnemyActor, "party_member")
        if self.loot is not None:
            ensure_type(self.loot, object, "loot")

        # Super Because of Generics Gymnastics
        super().__post_init__()


@dataclass(kw_only=True, slots=True)
class PlayerParty(CombatantParty[PlayableActor]):
    members: list[PlayableActor]
    dead_members: list[PlayableActor] = field(default_factory=list)
    relics: object | None = None

    def __post_init__(self):
        ensure_type(self.name, str, "name")
        ensure_type(self.members, list, "members")
        for party_member in self.members:
            ensure_type(party_member, PlayableActor, "party_member")
        if self.relics is not None:
            ensure_type(self.relics, object, "loot")

        # Super Because of Generics Gymnastics
        super().__post_init__()

    def end_game_report(self) -> str:
        player_report = ""
        for player_instance in self.members:
            player_report += f"""
    Player Name: {player_instance.name}
    Player Base Health: {player_instance.base_health}                             
    Player Final Health: {player_instance.health}
    Player Int: {player_instance.intellect}
    Player Str: {player_instance.strength}
    Player Agl: {player_instance.agility}
    Player Lck: {player_instance.luck}
    Player Gold: {player_instance.inventory.gold}
    Player Potions: {player_instance.inventory.potions}
    Player Attack Name: {player_instance.attack_name}
    Player Attack Power: {player_instance.attack_power}
    """

        player_report += "Fallen Members\n\n"

        for player_instance in self.dead_members:
            player_report += f"""
    Player Name: {player_instance.name}
    Player Base Health: {player_instance.base_health}                             
    Player Final Health: {player_instance.health}
    Player Int: {player_instance.intellect}
    Player Str: {player_instance.strength}
    Player Agl: {player_instance.agility}
    Player Lck: {player_instance.luck}
    Player Gold: {player_instance.inventory.gold}
    Player Potions: {player_instance.inventory.potions}
    Player Attack Name: {player_instance.attack_name}
    Player Attack Power: {player_instance.attack_power}
    """

        return player_report
