import json
import os
from dataclasses import dataclass
from typing import Any, Self

from content.dungeon_library import DungeonLibrary
from content.encounter_library import EncounterLibrary
from content.enemy_library import EnemyLibrary
from content.story_library import StoryLibrary
from utilites import ensure_type


@dataclass
class ContentPaths:
    standard_dungeons_path: str
    special_dungeons_path: str
    standard_encounters_path: str
    special_encounters_path: str
    standard_enemies_path: str
    special_enemies_path: str
    story_path: str


class ContentLibrary(
    EnemyLibrary,
    EncounterLibrary,
    DungeonLibrary,
    StoryLibrary,
):
    """
    Unified Content library that inherits from all the specalized libraries.
    Inheritence was chosen over composition to keep the object near the surface rather than burying the data 6 levels deep i.e.
    content_library.enemy_libary.small_enemies[0]
    """

    # Only the leaf class (the furthest out on the inheritence tree) can define slots, and you can't get fancy with concatenaed tuples to just stack them.
    __slots__ = (
        "small_enemies",
        "medium_enemies",
        "large_enemies",
        "special_enemies",
        "standard_encounters",
        "special_encounters",
        "standard_dungeons",
        "special_dungeons",
        "story_events",
        "_initialized",
    )
    _initialized: bool
    _instance: Self | None

    @staticmethod
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
                        conflicts = set(content_object.keys()).intersection(
                            set(combined_content.keys())
                        )
                    if conflicts == set():
                        combined_content.update(content_object)
                    else:
                        raise ValueError(
                            f"Duplicate Key Declaration found while processing {file_path} conflicting keys {conflicts}"
                        )

        return combined_content

    def __init__(self, content_paths: ContentPaths):
        EnemyLibrary.__init__(
            self,
            standard_enemies_data=ContentLibrary.load_content_files(
                content_paths.standard_enemies_path
            ),
            special_enemies_data=ContentLibrary.load_content_files(
                content_paths.special_enemies_path
            ),
        )
        EncounterLibrary.__init__(
            self,
            standard_encounters_data=ContentLibrary.load_content_files(
                content_paths.standard_encounters_path
            ),
            special_encounters_data=ContentLibrary.load_content_files(
                content_paths.special_encounters_path
            ),
        )
        DungeonLibrary.__init__(
            self,
            standard_dungeons_data=ContentLibrary.load_content_files(
                content_paths.standard_dungeons_path
            ),
            special_dungeons_data=ContentLibrary.load_content_files(
                content_paths.special_dungeons_path
            ),
        )
        StoryLibrary.__init__(
            self, event_data=ContentLibrary.load_content_files(content_paths.story_path)
        )

        self._initialized = True
        ContentLibrary._instance = self

    @classmethod
    def get_library(cls) -> "ContentLibrary":
        """
        Gateway style function to access the content library as a global singleton, you should not store the instance when init-ing
        Rather use this funciton to inject access at the lowest needed scope
        """
        if cls._instance._initialized is True:
            return cls._instance
        else:
            print(cls._instance._initialized)
            raise RuntimeError(
                "Attempted to access ContentLibrary before initialization has completed"
            )
