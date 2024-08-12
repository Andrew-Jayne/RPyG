from actors.actor import Actor
from utilites.utilities import ensure_type

# Only for Type Checking/Hinting
from actors.actor_combatant import Combatant
from actors.actor_playable import PlayableActor
from actors.actor_enemy import Enemy


class Party:
    def __init__(self, members: list[Actor]) -> None:
        ensure_type(members, list, 'members')

        for party_member in members:
            ensure_type(party_member, Actor, 'party_member')

        self.members = members

    def lose_member(self, member) -> None:
        self.members.remove(member)

    def gain_member(self, member) -> None:
        self.members.append(member)


class PlayerParty(Party):
    """
    Stores the progress of the party, and a list/array of member instances
    """

    def __init__(self, name: str, members: list[PlayableActor]) -> None:
        ensure_type(name, str, 'name')
        ensure_type(members, list, 'members')
        for party_member in members:
            ensure_type(party_member, PlayableActor, 'party_member' )

        Party.__init__(self, members=members)
        self.dead_members = []
        self.progress = 0
        self.name = name

    def lose_member(self, member) -> None:
        self.dead_members.append(member)
        self.members.remove(member)

    def gain_member(self, member) -> None:
        self.members.append(member)


class EnemyParty(Party):
    def __init__(self, name: str, members: list[Enemy]) -> None:
        ensure_type(name, str, 'name')
        ensure_type(members, list, 'members')
        for party_member in members:
            ensure_type(party_member, Enemy, 'party_member')

        Party.__init__(self, members=members)
        self.name = name
        self.members = members
