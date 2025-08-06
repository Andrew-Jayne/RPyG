from RPyG.actors.actor_combatant import Combatant, CombatantParty
from RPyG.utilites import ensure_type


class Enemy(Combatant):
    name: str
    health: int
    strength: int
    intellect: int
    agility: int
    luck: int
    attack_name: str
    is_special: bool

    def __init__(
        self,
        name: str,
        health: int,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
        attack_name: str,
        is_special: bool,
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(health, int, "health")
        ensure_type(strength, int, "'strength")
        ensure_type(intellect, int, "'intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(is_special, bool, "is_special")
        self.is_special = is_special

        Combatant.__init__(
            self,
            name=name,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
            health=health,
            attack_name=attack_name,
            attack_power=Enemy._set_enemy_attack_power(
                strength,
                intellect,
            ),
            special_attack_name=None,
            specialization="",
        )

    @staticmethod
    def _set_enemy_attack_power(strength: int, intellect: int) -> int:
        if strength >= 6 and intellect >= 6:
            attack_power = strength + intellect
        elif strength > intellect:
            attack_power = strength
        elif strength < intellect:
            attack_power = intellect
        else:
            attack_power = int((strength + intellect) / 2)

        return attack_power * 10


class EnemyParty(CombatantParty[Enemy]):
    members: list[Enemy]
    dead_members: list[Enemy]
    loot: object

    def __init__(
        self,
        name: str,
        members: list[Enemy],
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(members, list, "members")
        for party_member in members:
            ensure_type(party_member, Enemy, "party_member")

        ## super() Must be used because of typing and use of generics
        super().__init__(
            name=name,
            members=members,
        )

        self.loot = None
