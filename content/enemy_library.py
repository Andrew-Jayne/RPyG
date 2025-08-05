import random
from enum import Enum
from typing import Any

from actors import Enemy, EnemyParty
from utilites import ensure_type


class EnemyVariantSet:
    __slots__: tuple = ("lesser_variants", "common_variants", "greater_variants")
    lesser_variants: list[Enemy]
    common_variants: list[Enemy]
    greater_variants: list[Enemy]

    @staticmethod
    def validate_variant_data(variant_data: list[dict[str, Any]]) -> None:
        ensure_type(variant_data, list, "lesser_variants_data")
        for variant_data_item in variant_data:
            ensure_type(variant_data_item, dict, "variant_data_item")
            for variant_data_item_key in variant_data_item.keys():
                ensure_type(variant_data_item_key, str, "variant_data_item_key")

    @staticmethod
    def build_enemies(enemy_data_list: list[dict[str, Any]]) -> list[Enemy]:
        enemy_list: list[Enemy] = []
        for enemy_data in enemy_data_list:
            enemy_list.append(Enemy(**enemy_data))

        return enemy_list

    def __init__(
        self,
        lesser_variants_data: list[dict[str, Any]],
        common_variants_data: list[dict[str, Any]],
        greater_variants_data: list[dict[str, Any]],
    ) -> None:
        EnemyVariantSet.validate_variant_data(lesser_variants_data)
        EnemyVariantSet.validate_variant_data(common_variants_data)
        EnemyVariantSet.validate_variant_data(greater_variants_data)

        self.lesser_variants = EnemyVariantSet.build_enemies(lesser_variants_data)
        self.common_variants = EnemyVariantSet.build_enemies(common_variants_data)
        self.greater_variants = EnemyVariantSet.build_enemies(greater_variants_data)


class EnemyWeightClass(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    SPECIAL = "SPECIAL"


class EnemySet:
    __slots__: tuple = ("plural_name", "group_name", "weight_class", "variant_lists")
    plural_name: str
    group_name: str
    weight_class: EnemyWeightClass
    variant_lists: EnemyVariantSet

    @staticmethod
    def generate_enemy_party(enemy_set: "EnemySet", enemy_count: int) -> EnemyParty:
        from content.enemy_library import EnemySet

        ensure_type(enemy_set, EnemySet, "enemy_party_attributes")
        ensure_type(enemy_count, int, "enemy_count")

        # Create Instances & Add to Instance List
        enemy_party_instances: list[Enemy] = []
        for _ in range(0, enemy_count):
            variant_lists: list[list[Enemy]] = [
                enemy_set.variant_lists.lesser_variants,
                enemy_set.variant_lists.common_variants,
                enemy_set.variant_lists.greater_variants,
            ]

            active_variant_list: list[Enemy] = random.choice(variant_lists)

            variant_choice: Enemy = random.choice(active_variant_list)

            enemy_party_instances.append(variant_choice)
        if enemy_count == 1:
            enemy_party_name = f"Lone {enemy_party_instances[0].name}"
        else:
            enemy_party_name = (
                f"{enemy_set.group_name} of {enemy_count} {enemy_set.plural_name}"
            )

        return EnemyParty(enemy_party_name, enemy_party_instances)

    def __init__(
        self,
        plural_name: str,
        group_name: str,
        weight_class: str,
        variant_lists_data: dict[str, list[Any]],
    ) -> None:
        ensure_type(plural_name, str, "plural_name")
        ensure_type(group_name, str, "group_name")
        ensure_type(weight_class, str, "weight_class")
        ensure_type(variant_lists_data, dict, "variant_lists_data")
        for variant_lists_data_key in variant_lists_data.keys():
            ensure_type(variant_lists_data_key, str, "variant_lists_data_key")
        for variant_lists_data_value in variant_lists_data.values():
            ensure_type(variant_lists_data_value, list, "variant_lists_data_value")

        self.plural_name = plural_name
        self.group_name = group_name
        self.weight_class = EnemyWeightClass(weight_class)
        self.variant_lists = EnemyVariantSet(**variant_lists_data)


class EnemyLibrary:
    __slots__: tuple = (
        "small_enemies",
        "medium_enemies",
        "large_enemies",
        "special_enemies",
    )
    small_enemies: list[EnemySet]
    medium_enemies: list[EnemySet]
    large_enemies: list[EnemySet]
    special_enemies: dict[str, Enemy]

    @staticmethod
    def validate_enemy_list(enemy_list: list[dict[str, Any]], list_name: str) -> None:
        ensure_type(enemy_list, list, list_name)
        for enemy_list_item in enemy_list:
            ensure_type(enemy_list_item, dict, f"{list_name}_item")
            for enemy_item_key in enemy_list_item.keys():
                ensure_type(enemy_item_key, str, f"{list_name}item_key")

    @staticmethod
    def build_enemy_sets(enemy_set_data_list: list[dict[str, Any]]) -> list[EnemySet]:
        enemy_set: list[EnemySet] = []
        for enemy_set_data in enemy_set_data_list:
            enemy_set.append(EnemySet(**enemy_set_data))
        return enemy_set

    @staticmethod
    def sort_standard_enemies(
        raw_enemy_data: dict[str, dict[str, Any]],
    ) -> tuple[
        list[dict[str, Any]],
        list[dict[str, Any]],
        list[dict[str, Any]],
    ]:
        # behold Run time safe dict loading (totaly easier than using a data class)
        ensure_type(raw_enemy_data, dict, "raw_enemy_data")
        for item_key in raw_enemy_data.keys():
            ensure_type(item_key, str, "item_key")
        for item_value in raw_enemy_data.values():
            ensure_type(item_value, dict, "item_value")

        small_enemies_data: list[dict[str, Any]] = []
        medium_enemies_data: list[dict[str, Any]] = []
        large_enemies_data: list[dict[str, Any]] = []
        for item in raw_enemy_data.values():
            match EnemyWeightClass(item["weight_class"]):
                case EnemyWeightClass.SMALL:
                    small_enemies_data.append(item)
                case EnemyWeightClass.MEDIUM:
                    medium_enemies_data.append(item)
                case EnemyWeightClass.LARGE:
                    large_enemies_data.append(item)
                case EnemyWeightClass.SPECIAL:
                    pass
                case _:
                    raise ValueError(
                        f"Got Invalid weight class {item.get('weight_class')}"
                    )

        return (small_enemies_data, medium_enemies_data, large_enemies_data)

    def __init__(
        self,
        standard_enemies_data: dict[str, list[dict[str, Any]]],
        special_enemies_data: dict[str, Any],
    ) -> None:
        ensure_type(special_enemies_data, dict, "special_enemies_data")
        for special_enemies_data_key in special_enemies_data.keys():
            ensure_type(special_enemies_data_key, str, "special_enemies_data_key")
        ## ick I don't like returning tuples but this just makes more sense than returning a dict, then indexing into it
        small_enemies_data, medium_enemies_data, large_enemies_data = (
            EnemyLibrary.sort_standard_enemies(standard_enemies_data)
        )
        EnemyLibrary.validate_enemy_list(small_enemies_data, "small_enemies_data")
        EnemyLibrary.validate_enemy_list(medium_enemies_data, "medium_enemies_data")
        EnemyLibrary.validate_enemy_list(large_enemies_data, "large_enemies_data")

        self.small_enemies = EnemyLibrary.build_enemy_sets(small_enemies_data)
        self.medium_enemies = EnemyLibrary.build_enemy_sets(medium_enemies_data)
        self.large_enemies = EnemyLibrary.build_enemy_sets(large_enemies_data)

        special_enemies_instances: dict[str, Enemy] = {}
        for enemy_id, enemy_data in special_enemies_data.items():
            special_enemies_instances[enemy_id] = Enemy(**enemy_data)
        self.special_enemies = special_enemies_instances
