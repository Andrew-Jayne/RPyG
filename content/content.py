import json
import os
from typing import Any, Final

from content.enemy_library import EnemyLibrary
from content.encounter_library import EncounterLibrary
from utilites import ensure_type


DUNGEONS_STANDARD_PATH = "content/dungeons/standard"
DUNGEONS_SPECIAL_PATH = "content/dungeons/special"

ENCOUNTERS_STANDARD_PATH = "content/encounters/standard"
ENCOUNTERS_SPECIAL_PATH = "content/encounters/special"

ENEMIES_STANDARD_PATH = "content/enemies/standard"
ENEMIES_SPECIAL_PATH = "content/enemies/special"

STORY_PATH = "content/story"


def load_content_files(dir_path: str) -> dict[str, dict[str, Any]]:
    """
    Load all JSON files in the given directory and merge their contents into a single dictionary.
    """
    combined_content: dict[str, dict[str, Any]] = {}

    # Walk through the directory and look for JSON files
    for root, _dirs, files in os.walk(dir_path):
        for file_name in files:
            if file_name.endswith(".json"):
                file_path = os.path.join(root, file_name)
                with open(file_path, "r") as file:
                    content_object: dict[str, dict[str, Any]] = json.load(file)
                    # Merge the content into the combined dictionary
                combined_content.update(content_object)

    return combined_content


def load_enemy_content(
    raw_enemy_data: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    # behold Run time safe dict loading (totaly easier than using a data class)
    ensure_type(raw_enemy_data, dict, "raw_enemy_data")
    for item_key in raw_enemy_data.keys():
        ensure_type(item_key, str, "item_key")
    for item_value in raw_enemy_data.values():
        ensure_type(item_value, dict, "item_value")

    processed_enemy_data: dict[str, list[dict[str, Any]]] = {
        "small_enemies_data": [],
        "medium_enemies_data": [],
        "large_enemies_data": [],
    }
    for item in raw_enemy_data.values():
        match item["weight_class"]:
            case "small":
                processed_enemy_data["small_enemies_data"].append(item)
            case "medium":
                processed_enemy_data["medium_enemies_data"].append(item)
            case "large":
                processed_enemy_data["large_enemies_data"].append(item)
            case _:
                raise ValueError(f"Got Invalid weight class {item.get('weight_class')}")

    return processed_enemy_data


DUNGEONS_STANDARD: Final = load_content_files(DUNGEONS_STANDARD_PATH)
DUNGEONS_SPECIAL: Final = load_content_files(DUNGEONS_SPECIAL_PATH)
ENCOUNTERS_STANDARD: Final[EncounterLibrary] = EncounterLibrary(
    encounters_data=load_content_files(ENCOUNTERS_STANDARD_PATH)
)
ENCOUNTERS_SPECIAL: Final = load_content_files(ENCOUNTERS_SPECIAL_PATH)
ENEMIES_STANDARD: Final[EnemyLibrary] = EnemyLibrary(
    **load_enemy_content(load_content_files(ENEMIES_STANDARD_PATH))
)
ENEMIES_SPECIAL: Final = load_content_files(ENEMIES_SPECIAL_PATH)
STORY: Final = load_content_files(STORY_PATH)
