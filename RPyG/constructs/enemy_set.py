import copy
import random
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.constructs import EnemyActor, EnemyParty


class EnemyVariantGrade(Enum):
    LESSER = "LESSER"
    COMMON = "COMMON"
    GREATER = "GREATER"
    LEGENDARY = "LEGENDARY"
    SPECIAL = "SPECIAL"


class EnemyWeightClass(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    SPECIAL = "SPECIAL"


class EnemySetType(Enum):
    STANDARD = "STANDARD"
    SPECIAL = "SPECIAL"


class EnemySet:
    plural_name: str
    group_name: str
    set_type: EnemySetType
    weight_class: EnemyWeightClass
    enemy_ids: list[str]
    key_enemy_id: str | None

    def __init__(
        self,
        kind: str,
        plural_name: str,
        group_name: str,
        weight_class: str,
        set_type: str,
        enemy_ids: list[str],
        key_enemy_id: str | None = None,
    ) -> None:
        ensure_type(kind, str, "kind")
        ensure_type(plural_name, str, "plural_name")
        ensure_type(group_name, str, "group_name")
        ensure_type(weight_class, str, "weight_class")
        ensure_type(set_type, str, "set_type")
        ensure_type(enemy_ids, list, "enemy_ids")
        for enemy_id in enemy_ids:
            ensure_type(enemy_id, str, "enemy_id")

        if key_enemy_id is not None:
            ensure_type(key_enemy_id, str, "key_enemy_id")

        self.plural_name = plural_name
        self.group_name = group_name
        self.weight_class = EnemyWeightClass(weight_class)
        self.set_type = EnemySetType(set_type)
        self.enemy_ids = enemy_ids
        self.key_enemy_id = key_enemy_id

    @cached_property
    def variants_by_grade(self) -> dict[EnemyVariantGrade, list[EnemyActor]]:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()

        enemy_party_instances: list[EnemyActor] = []
        # select enemy ids from the enemy library
        for enemy_id in self.enemy_ids:
            enemy_party_instances.append(library.enemies[enemy_id])

        variant_lists: dict[EnemyVariantGrade, list[EnemyActor]] = {
            EnemyVariantGrade.LESSER: [],
            EnemyVariantGrade.COMMON: [],
            EnemyVariantGrade.GREATER: [],
            EnemyVariantGrade.LEGENDARY: [],
            EnemyVariantGrade.SPECIAL: [],
        }

        for variant in enemy_party_instances:
            match variant.variant_grade:
                case EnemyVariantGrade.LESSER:
                    variant_lists[EnemyVariantGrade.LESSER].append(variant)
                case EnemyVariantGrade.COMMON:
                    variant_lists[EnemyVariantGrade.COMMON].append(variant)
                case EnemyVariantGrade.GREATER:
                    variant_lists[EnemyVariantGrade.GREATER].append(variant)
                case EnemyVariantGrade.LEGENDARY:
                    variant_lists[EnemyVariantGrade.LEGENDARY].append(variant)
                case EnemyVariantGrade.SPECIAL:
                    variant_lists[EnemyVariantGrade.SPECIAL].append(variant)
                case _:  # pyright: ignore[reportUnnecessaryComparison]
                    raise ValueError()  # pyright: ignore[reportUnreachable]

        return variant_lists

    @cached_property
    def key_enemy(self) -> EnemyActor | None:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()
        if self.key_enemy_id is not None:
            return library.enemies[self.key_enemy_id]
        return None

    def generate_enemy_party(
        self,
        enemy_count: int,
    ) -> EnemyParty:
        from RPyG.constructs import EnemyParty, RandomResultItem, RandomResultTable

        ensure_type(enemy_count, int, "enemy_count")

        enemy_party_instances: list[EnemyActor] = []
        if self.key_enemy is not None:
            enemy_party_instances.append(self.key_enemy)

        # select random grade of enemy on each attempt, 1 in 25 chance of legendary (will have loot later))
        grade_table = RandomResultTable(
            [
                RandomResultItem(EnemyVariantGrade.LEGENDARY, (1 / 25)),
                RandomResultItem(EnemyVariantGrade.LESSER, (1 / 3)),
                RandomResultItem(EnemyVariantGrade.COMMON, (1 / 3)),
                RandomResultItem(EnemyVariantGrade.GREATER, (1 / 3)),
            ]
        )

        for _ in range(0, enemy_count):
            enemy_grade = grade_table.generate_result()
            enemy_party_instances.append(
                copy.deepcopy(random.choice(self.variants_by_grade[enemy_grade]))
            )

        if len(enemy_party_instances) == 1:
            enemy_party_name = f"Lone {enemy_party_instances[0].name}"
        else:
            enemy_party_name = f"{self.group_name} of {enemy_count} {self.plural_name}"

        return EnemyParty(enemy_party_name, enemy_party_instances)

    def validate(self) -> bool:
        from RPyG.constructs import EnemyActor

        ensure_type(self.plural_name, str, "self.plural_name")
        ensure_type(self.group_name, str, "self.group_name")
        ensure_type(self.set_type, EnemySetType, "self.set_type")
        ensure_type(self.weight_class, EnemyWeightClass, "self.weight_class")

        key_enemy = self.key_enemy
        if key_enemy is not None:
            ensure_type(key_enemy, EnemyActor, "key_enemy")

        variants_by_grade = self.variants_by_grade
        ensure_type(variants_by_grade, dict, "variants_by_grade")
        for grade, enemy_list in variants_by_grade.items():
            ensure_type(grade, EnemyVariantGrade, "grade")
            ensure_type(enemy_list, list, "enemy_list")
            for enemy in enemy_list:
                if enemy_list == []:
                    return False
                ensure_type(enemy, EnemyActor, "enemy")

        return True
