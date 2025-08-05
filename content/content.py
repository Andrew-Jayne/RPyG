import json
import os
from typing import Any, Final

from content.dungeon_library import DungeonLibrary
from content.encounter_library import EncounterLibrary
from content.enemy_library import EnemyLibrary
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
    ensure_type(dir_path, str, "dir_path")
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


DUNGEONS = ""
ENCOUTNERS = ""
ENEMIES: Final[EnemyLibrary] = EnemyLibrary(
    special_enemies_data=load_content_files(ENEMIES_SPECIAL_PATH),
    standard_enemies_data=load_content_files(ENEMIES_STANDARD_PATH),
)
ENCOUNTERS: Final[EncounterLibrary] = EncounterLibrary(
    standard_encounters_data=load_content_files(ENCOUNTERS_STANDARD_PATH),
    special_encounters_data=load_content_files(ENCOUNTERS_SPECIAL_PATH),
)

DUNGEONS: Final[DungeonLibrary] = DungeonLibrary(
    standard_dungeons_data=load_content_files(DUNGEONS_STANDARD_PATH),
    special_dungeons_data=load_content_files(DUNGEONS_SPECIAL_PATH),
)

STORY: Final = load_content_files(STORY_PATH)
