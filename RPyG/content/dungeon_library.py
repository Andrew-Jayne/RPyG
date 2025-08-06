from typing import Any

from RPyG.encounters.encounter_dungeon import Dungeon
from RPyG.utilites import ensure_type


class DungeonLibrary:
    standard_dungeons: dict[str, Dungeon]
    special_dungeons: dict[str, Dungeon]

    @staticmethod
    def generate_dungeon_instances(dungeon_data: dict[str, Any]) -> dict[str, Dungeon]:
        dungeon_content: dict[str, Dungeon] = {}
        for dungeon_id, dungeon_item in dungeon_data.items():
            dungeon_content[dungeon_id] = Dungeon(**dungeon_item)

        return dungeon_content

    @staticmethod
    def validate_dungeon_data(dungeon_data: dict[str, Any]) -> None:
        ensure_type(dungeon_data, dict, "dungeon_data")
        for dungeon_data_key in dungeon_data.keys():
            ensure_type(dungeon_data_key, str, "dungeon_data_key")

    def __init__(
        self,
        standard_dungeons_data: dict[str, Any],
        special_dungeons_data: dict[str, Any],
    ) -> None:
        DungeonLibrary.validate_dungeon_data(standard_dungeons_data)
        DungeonLibrary.validate_dungeon_data(special_dungeons_data)
        self.standard_dungeons = DungeonLibrary.generate_dungeon_instances(
            standard_dungeons_data
        )
        self.special_dungeons = DungeonLibrary.generate_dungeon_instances(
            special_dungeons_data
        )
