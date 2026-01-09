from enum import Enum

from RPyG.actors.actor_combatant import Combatant, CombatantParty
from RPyG.utilities import ensure_type


class EnemyVariantGrade(Enum):
    LESSER = "LESSER"
    COMMON = "COMMON"
    GREATER = "GREATER"
    LEGENDARY = "LEGENDARY"
    SPECIAL = "SPECIAL"


class Enemy(Combatant):
    name: str
    health: int
    strength: int
    intellect: int
    agility: int
    luck: int
    attack_name: str
    is_special: bool
    variant_grade: EnemyVariantGrade

    def __init__(
        self,
        kind: str,
        name: str,
        health: int,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
        attack_name: str,
        is_special: bool,
        variant_grade: str,
    ) -> None:
        ensure_type(name, str, "name")
        ensure_type(health, int, "health")
        ensure_type(strength, int, "'strength")
        ensure_type(intellect, int, "'intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(is_special, bool, "is_special")

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

        self.is_special = is_special
        self.variant_grade = EnemyVariantGrade(variant_grade)

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

    def validate(self) -> bool:
        ensure_type(self.name, str, "self.name")
        ensure_type(self.health, int, "self.health")
        ensure_type(self.strength, int, "self.strength")
        ensure_type(self.intellect, int, "self.intellect")
        ensure_type(self.agility, int, "self.agility")
        ensure_type(self.luck, int, "self.luck")
        ensure_type(self.attack_name, str, "self.attack_name")
        ensure_type(self.is_special, bool, "self.is_special")
        ensure_type(self.variant_grade, EnemyVariantGrade, "self.variant_grade")
        return True


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
