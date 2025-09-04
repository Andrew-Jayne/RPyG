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


class SetType(Enum):
    STANDARD = "STANDARD"
    SPECIAL = "SPECIAL"


class EnemySet:
    plural_name: str
    group_name: str
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
        self.set_type = SetType(set_type)
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


# from types import MappingProxyType
# from typing import Any

# from RPyG.actors import Enemy
# from RPyG.constructs import EnemySet
# from RPyG.utilites import ensure_type


# class EnemyLibrary:
#     enemies: dict[str, Enemy]
#     enemy_sets: dict[str, EnemySet]
#     _enemy_set_definitions: dict[str, Any]
#     small_enemies: tuple[EnemySet, ...]
#     medium_enemies: tuple[EnemySet, ...]
#     large_enemies: tuple[EnemySet, ...]
#     special_enemies: MappingProxyType[str, Enemy]

#     @staticmethod
#     def validate_enemy_list(enemy_list: list[dict[str, Any]], list_name: str) -> None:
#         ensure_type(enemy_list, list, list_name)
#         for enemy_list_item in enemy_list:
#             ensure_type(enemy_list_item, dict, f"{list_name}_item")
#             for enemy_item_key in enemy_list_item.keys():
#                 ensure_type(enemy_item_key, str, f"{list_name}item_key")

#     @staticmethod
#     def build_enemy_sets(enemy_set_data_list: list[dict[str, Any]]) -> tuple[EnemySet]:
#         enemy_sets: list[EnemySet] = []
#         for enemy_set_data in enemy_set_data_list:
#             enemy_sets.append(EnemySet(**enemy_set_data))
#         return tuple(enemy_sets)

#     @staticmethod
#     def sort_standard_enemies(
#         raw_enemy_data: dict[str, dict[str, Any]],
#     ) -> tuple[
#         list[dict[str, Any]],
#         list[dict[str, Any]],
#         list[dict[str, Any]],
#     ]:
#         # behold Run time safe dict loading (totaly easier than using a data class)
#         ensure_type(raw_enemy_data, dict, "raw_enemy_data")
#         for item_key in raw_enemy_data.keys():
#             ensure_type(item_key, str, "item_key")
#         for item_value in raw_enemy_data.values():
#             ensure_type(item_value, dict, "item_value")

#         small_enemies_data: list[dict[str, Any]] = []
#         medium_enemies_data: list[dict[str, Any]] = []
#         large_enemies_data: list[dict[str, Any]] = []
#         for item in raw_enemy_data.values():
#             match EnemyWeightClass(item["weight_class"]):
#                 case EnemyWeightClass.SMALL:
#                     small_enemies_data.append(item)
#                 case EnemyWeightClass.MEDIUM:
#                     medium_enemies_data.append(item)
#                 case EnemyWeightClass.LARGE:
#                     large_enemies_data.append(item)
#                 case EnemyWeightClass.SPECIAL:
#                     pass
#                 case _:
#                     raise ValueError(
#                         f"Got Invalid weight class {item.get('weight_class')}"
#                     )

#         return (small_enemies_data, medium_enemies_data, large_enemies_data)

#     def __init__(
#         self,
#         standard_enemies_data: dict[str, Any],
#         special_enemies_data: dict[str, Any],
#     ) -> None:
#         ensure_type(special_enemies_data, dict, "special_enemies_data")
#         for special_enemies_data_key in special_enemies_data.keys():
#             ensure_type(special_enemies_data_key, str, "special_enemies_data_key")
#         ## ick I don't like returning tuples but this just makes more sense than returning a dict, then indexing into it
#         small_enemies_data, medium_enemies_data, large_enemies_data = (
#             EnemyLibrary.sort_standard_enemies(standard_enemies_data)
#         )
#         EnemyLibrary.validate_enemy_list(small_enemies_data, "small_enemies_data")
#         EnemyLibrary.validate_enemy_list(medium_enemies_data, "medium_enemies_data")
#         EnemyLibrary.validate_enemy_list(large_enemies_data, "large_enemies_data")

#         self.small_enemies = EnemyLibrary.build_enemy_sets(small_enemies_data)
#         self.medium_enemies = EnemyLibrary.build_enemy_sets(medium_enemies_data)
#         self.large_enemies = EnemyLibrary.build_enemy_sets(large_enemies_data)

#         special_enemies_instances: dict[str, Enemy] = {}
#         for enemy_id, enemy_data in special_enemies_data.items():
#             special_enemies_instances[enemy_id] = Enemy(**enemy_data)
#         self.special_enemies = MappingProxyType(special_enemies_instances)

#     def add_enemy_set_definition(self, enemy_set_data: dict[str, Any]) -> None:
#         """
#         Adds the Definition to a cache of set data, once all content is loaded use
#         finalize_enemy_sets() to generate the enemy set objects
#         """
#         pass

#     def add_enemy(self, enemy_data: dict[str, Any]) -> None:
#         pass

#     def finalize_enemy_sets(self) -> None:
#         """
#         Builds the final enemy sets once all content files have been loaded
#         Need to make this a 2 step because otherwise the order of files and items in them can cause errors
#         that is puts to much power into the arangement of data, when only the data should matter
#         """
#         pass
