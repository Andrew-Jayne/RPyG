from typing import Any

from actors import Enemy
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


class EnemySet:
    __slots__: tuple = ("pural_name", "group_name", "weight_class", "variant_lists")
    pural_name: str
    group_name: str
    weight_class: str
    variant_lists: EnemyVariantSet

    def __init__(
        self,
        pural_name: str,
        group_name: str,
        weight_class: str,
        variant_lists_data: dict[str, list[Any]],
    ) -> None:
        ensure_type(pural_name, str, "pural_name")
        ensure_type(group_name, str, "group_name")
        ensure_type(weight_class, str, "weight_class")
        ensure_type(variant_lists_data, dict, "variant_lists_data")
        for variant_lists_data_key in variant_lists_data.keys():
            ensure_type(variant_lists_data_key, str, "variant_lists_data_key")
        for variant_lists_data_value in variant_lists_data.values():
            ensure_type(variant_lists_data_value, list, "variant_lists_data_value")

        self.pural_name = pural_name
        self.group_name = group_name
        self.weight_class = weight_class
        self.variant_lists = EnemyVariantSet(**variant_lists_data)


class EnemyLibrary:
    __slots__: tuple = ("small_enemies", "medium_enemies", "large_enemies")
    small_enemies: list[EnemySet]
    medium_enemies: list[EnemySet]
    large_enemies: list[EnemySet]

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

    def __init__(
        self,
        small_enemies_data: list[dict[str, Any]],
        medium_enemies_data: list[dict[str, Any]],
        large_enemies_data: list[dict[str, Any]],
    ) -> None:
        EnemyLibrary.validate_enemy_list(small_enemies_data, "small_enemies_data")
        EnemyLibrary.validate_enemy_list(medium_enemies_data, "medium_enemies_data")
        EnemyLibrary.validate_enemy_list(large_enemies_data, "large_enemies_data")

        self.small_enemies = EnemyLibrary.build_enemy_sets(small_enemies_data)
        self.medium_enemies = EnemyLibrary.build_enemy_sets(medium_enemies_data)
        self.large_enemies = EnemyLibrary.build_enemy_sets(large_enemies_data)
