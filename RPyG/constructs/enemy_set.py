import random
from enum import Enum
from functools import cached_property

from RPyG.actors import Enemy, EnemyParty, EnemyVariantGrade
from RPyG.utilites import ensure_type


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

    # this function is painful, and needs to be reworked
    def generate_enemy_party(
        self,
        enemy_count: int,
    ) -> EnemyParty:
        ensure_type(enemy_count, int, "enemy_count")

        # select random grade of enemy on each attempt, 1 in 25 chance of legendary (will have loot later))
        enemy_party_instances: list[Enemy] = []
        if self.key_enemy is not None:
            enemy_party_instances.append(self.key_enemy)

        for _ in range(0, enemy_count):
            match random.randint(1, 25):
                case 25:
                    enemy_party_instances.append(
                        random.choice(
                            self.variants_by_grade[EnemyVariantGrade.LEGENDARY]
                        )
                    )
                case _:
                    ## BARF WHY DID I DO THIS
                    enemy_party_instances.append(
                        random.choice(
                            self.variants_by_grade[
                                random.choice(
                                    [
                                        EnemyVariantGrade.LESSER,
                                        EnemyVariantGrade.COMMON,
                                        EnemyVariantGrade.GREATER,
                                    ]
                                )
                            ]
                        )
                    )

        if len(enemy_party_instances) == 1:
            enemy_party_name = f"Lone {enemy_party_instances[0].name}"
        else:
            enemy_party_name = f"{self.group_name} of {enemy_count} {self.plural_name}"

        return EnemyParty(enemy_party_name, enemy_party_instances)

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
        self.plural_name = plural_name
        self.group_name = group_name
        self.weight_class = EnemyWeightClass(weight_class)
        self.set_type = EnemySetType(set_type)
        self.enemy_ids = enemy_ids
        self.key_enemy_id = key_enemy_id

    @cached_property
    def variants_by_grade(self) -> dict[EnemyVariantGrade, list[Enemy]]:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()

        enemy_party_instances: list[Enemy] = []
        # select enemy ids from the enemy library
        for enemy_id in self.enemy_ids:
            enemy_party_instances.append(library.enemies[enemy_id])

        variant_lists: dict[EnemyVariantGrade, list[Enemy]] = {
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
                case _:
                    raise ValueError()

        return variant_lists

    @cached_property
    def key_enemy(self) -> Enemy | None:
        from RPyG.content import ContentLibrary

        library = ContentLibrary.get_library()
        if self.key_enemy_id is not None:
            return library.enemies[self.key_enemy_id]
        return None

    def validate(self) -> bool:
        _variants = self.variants_by_grade
        _key_enemy = self.key_enemy
        return True
