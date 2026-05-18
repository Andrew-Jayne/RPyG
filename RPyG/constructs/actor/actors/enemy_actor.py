from typing import TYPE_CHECKING

from RPyG.constructs.actor.actors.combatant_actor import CombatantActor
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs import EnemyVariantGrade


class EnemyActor(CombatantActor):
    is_special: bool
    variant_grade: EnemyVariantGrade
    __slots__: tuple[str, ...] = ("is_special", "variant_grade")

    @classmethod
    def build(
        cls,
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
    ) -> EnemyActor:

        ensure_type(kind, str, "kind")
        ensure_type(name, str, "name")
        ensure_type(health, int, "health")
        ensure_type(strength, int, "strength")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(is_special, bool, "is_special")
        ensure_type(variant_grade, str, "variant_grade")
        return EnemyActor(
            name=name,
            health=health,
            base_health=health,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
            attack_name=attack_name,
            attack_power=EnemyActor._set_enemy_attack_power(
                strength,
                intellect,
            ),
            is_special=is_special,
            variant_grade=variant_grade,
        )

    def __init__(
        self,
        name: str,
        health: int,
        base_health: int,
        strength: int,
        intellect: int,
        agility: int,
        luck: int,
        attack_name: str,
        attack_power: int,
        is_special: bool,
        variant_grade: str,
        specialization: str = "",
        special_attack_name: str = "",
        special_attack_energy: int = 0,
        use_special_attack: bool = False,
        will_react: bool = False,
        is_dismembered: bool = False,
    ) -> None:
        from RPyG.constructs import EnemyVariantGrade

        ensure_type(name, str, "name")
        ensure_type(health, int, "health")
        ensure_type(base_health, int, "base_health")
        ensure_type(strength, int, "strength")
        ensure_type(intellect, int, "intellect")
        ensure_type(agility, int, "agility")
        ensure_type(luck, int, "luck")
        ensure_type(attack_name, str, "attack_name")
        ensure_type(attack_power, int, "attack_power")
        ensure_type(is_special, bool, "is_special")
        ensure_type(variant_grade, str, "variant_grade")

        CombatantActor.__init__(
            self,
            name=name,
            strength=strength,
            intellect=intellect,
            agility=agility,
            luck=luck,
            health=health,
            base_health=base_health,
            attack_name=attack_name,
            attack_power=attack_power,
            special_attack_name=special_attack_name,
            specialization=specialization,
            will_react=will_react,
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
        from RPyG.constructs import EnemyVariantGrade

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
