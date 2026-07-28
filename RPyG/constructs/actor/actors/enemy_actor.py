from dataclasses import dataclass
from typing import TYPE_CHECKING

from RPyG.constructs.actor.actors.combatant_actor import (
    CombatantActor,
    CombatantProperties,
)
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs import EnemyVariantGrade


@dataclass(frozen=True, slots=True, kw_only=True)
class EnemyProperties(CombatantProperties):
    kind: str
    is_special: bool
    variant_grade: EnemyVariantGrade

    def __post_init__(self):
        from RPyG.constructs import EnemyVariantGrade

        ensure_type(self.kind, str, "kind")
        ensure_type(self.is_special, bool, "is_special")
        ensure_type(self.variant_grade, EnemyVariantGrade, "variant_grade")
        CombatantProperties.__post_init__(self)


class EnemyActor(CombatantActor):
    is_special: bool
    variant_grade: EnemyVariantGrade
    __slots__: tuple[str, ...] = ("is_special", "variant_grade")

    def __init__(self, properties: EnemyProperties) -> None:
        CombatantActor.__init__(
            self,
            properties=properties,
        )

        self.is_special = properties.is_special
        self.variant_grade = properties.variant_grade

    def validate(self) -> bool:
        return True

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
        from RPyG.constructs import EnemyVariantGrade

        return EnemyActor(
            properties=EnemyProperties(
                name=name,
                kind=kind,
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
                special_attack_energy=0,
                is_special=is_special,
                variant_grade=EnemyVariantGrade(variant_grade),
                special_attack_name="",
                specialization="",
            )
        )
