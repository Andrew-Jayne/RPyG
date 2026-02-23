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


class ActorParty(Generic[ActorType]):
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


class CombatantParty(ActorParty[CombatantType], Generic[CombatantType]):
    name: str
    members: list[CombatantType]
    dead_members: list[CombatantType]

    def __init__(
        self,
        name: str,
        members: list[CombatantType],
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(members, list, "members")
        for party_member in members:
            ensure_type(party_member, CombatantActor, "party_member")

        if len(name) > 64:
            raise ValueError("Combatant Party name may not be longer than characters")

        ## super() Must be used because of typing and use of generics
        super().__init__(
            members=members,
        )
        self.name = name
        self.dead_members = []

    @override
    def lose_member(self, member: CombatantType) -> None:
        from RPyG.core_io import CoreIO, output_models

        core_io = CoreIO.get_core_io()
        core_io.send_output(
            output_models.OutputMessage(f"{member.name} has been defeated")
        )
        self.dead_members.append(member)
        self.members.remove(member)

    @override
    def gain_member(self, member: CombatantType) -> None:
        self.members.append(member)


class EnemyParty(CombatantParty[EnemyActor]):
    members: list[EnemyActor]
    dead_members: list[EnemyActor]
    loot: object

    def __init__(
        self,
        name: str,
        members: list[EnemyActor],
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(members, list, "members")
        for party_member in members:
            ensure_type(party_member, EnemyActor, "party_member")

        ## super() Must be used because of typing and use of generics
        super().__init__(
            name=name,
            members=members,
        )

        self.loot = None


class PlayerParty(CombatantParty[PlayableActor]):
    members: list[PlayableActor]
    dead_members: list[PlayableActor]
    relics: object
    """
    Stores the progress of the party, and a list/array of member instances
    """

    def __init__(
        self,
        name: str,
        members: list[PlayableActor],
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(members, list, "members")
        for party_member in members:
            ensure_type(party_member, PlayableActor, "party_member")

        ## super() Must be used because of typing and use of generics
        super().__init__(
            name=name,
            members=members,
        )
        self.relics = None

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
