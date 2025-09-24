import json
import os
import random
import tomllib
from enum import Enum
from functools import cached_property
from typing import Any

from RPyG.actors import Enemy
from RPyG.constructs import (
    Dungeon,
    Encounter,
    EncounterType,
    EnemySet,
    EnemySetType,
    EnemyWeightClass,
    StoryEvent,
)
from RPyG.utilites import ensure_type


class ContentKind(Enum):
    EnemySet = "EnemySet"
    Dungeon = "Dungeon"
    Enemy = "Enemy"
    Encounters = "Encounters"
    StoryEvent = "StoryEvent"


class ContentLibrary:
    enemies: dict[str, Enemy]
    enemy_sets: dict[str, EnemySet]
    story_events: dict[int, StoryEvent]
    encounters: dict[str, Encounter]
    dungeons: dict[str, Dungeon]
    _instance: "ContentLibrary | None" = None

    @staticmethod
    def build_story_events(story_events_data: dict[str, Any]) -> dict[int, StoryEvent]:
        all_events = {}
        for value in story_events_data.values():
            event = StoryEvent(**value)
            all_events[event.progress_trigger] = event

        return all_events

    @staticmethod
    def build_encounters(encounters_data: dict[str, Any]) -> dict[str, Encounter]:
        all_encouters = {}
        for key, value in encounters_data.items():
            all_encouters[key] = Encounter(**value)

        return all_encouters

    @staticmethod
    def build_enemy_sets(enemy_sets_data: dict[str, Any]) -> dict[str, EnemySet]:
        all_enemy_sets = {}
        for key, value in enemy_sets_data.items():
            all_enemy_sets[key] = EnemySet(**value)

        return all_enemy_sets

    @staticmethod
    def build_enemies(enemies_data: dict[str, Any]) -> dict[str, Enemy]:
        all_enemies = {}
        for key, value in enemies_data.items():
            all_enemies[key] = Enemy(**value)

        return all_enemies

    @staticmethod
    def build_dungeons(dungeons_data: dict[str, Any]) -> dict[str, Dungeon]:
        all_dungeons = {}
        for key, value in dungeons_data.items():
            all_dungeons[key] = Dungeon(**value)

        return all_dungeons

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
                file_path = os.path.join(root, file_name)
                file_extension = os.path.splitext(file_path)[1]
                content_object: dict[str, dict[str, Any]] = {}
                match file_extension:
                    case ".json":
                        with open(file_path, "r") as json_file:
                            content_object = json.load(json_file)
                    case ".toml":
                        with open(file_path, "rb") as toml_file:
                            content_object = tomllib.load(toml_file)
                    case _:
                        pass

                new_object = set(content_object.keys())
                all_content = set(combined_content.keys())
                conflicts = new_object.intersection(all_content)
                if conflicts == set():
                    combined_content.update(content_object)
                else:
                    raise ValueError(
                        f"Duplicate Key Declaration found while processing {file_path} conflicting keys {conflicts}"
                    )

        return combined_content

    def __init__(self, content_path: str):
        if ContentLibrary._instance is None:
            all_content = ContentLibrary.load_content_files(content_path)

            enemies_data = {}
            enemy_sets_data = {}
            dungeons_data = {}
            encounters_data = {}
            story_events_data = {}

            for item, value in all_content.items():
                try:
                    item_kind = ContentKind(
                        str(value["kind"]).split("/")[0]
                    )  # Added [0] to get first part after split
                except KeyError:
                    raise KeyError(f"Item {item} has no 'kind' value set")
                except ValueError:
                    raise ValueError(
                        f"Unknown content kind: {value['kind']}, for item {item}"
                    )

                match item_kind:
                    case ContentKind.EnemySet:
                        enemy_sets_data[item] = value
                    case ContentKind.Dungeon:
                        dungeons_data[item] = value
                    case ContentKind.Enemy:
                        enemies_data[item] = value
                    case ContentKind.Encounters:
                        encounters_data[item] = value
                    case ContentKind.StoryEvent:
                        story_events_data[item] = value
                    case _:
                        raise ValueError(
                            f"item {item} has unsupported kind {item_kind}"
                        )

            self.story_events = ContentLibrary.build_story_events(story_events_data)
            self.encounters = ContentLibrary.build_encounters(encounters_data)
            self.enemies = ContentLibrary.build_enemies(enemies_data)
            self.enemy_sets = ContentLibrary.build_enemy_sets(enemy_sets_data)
            self.dungeons = ContentLibrary.build_dungeons(dungeons_data)

            ContentLibrary._instance = self
        else:
            raise RuntimeError("ContentLibrary already initialized")

    @classmethod
    def get_library(cls) -> "ContentLibrary":
        """
        Gateway style function to access the content library as a global singleton, you should not store the instance when init-ing
        Rather use this funciton to inject access at the lowest needed scope
        """
        if ContentLibrary._instance is not None:
            return ContentLibrary._instance
        else:
            raise RuntimeError(
                "Attempted to access ContentLibrary before initialization has completed"
            )

    @classmethod
    def validate_content(cls) -> None:
        library = ContentLibrary.get_library()
        for story_event in library.story_events.values():
            story_event.validate()

        for encounter in library.encounters.values():
            encounter.validate()

        for enemy in library.enemies.values():
            enemy.validate()

        for enemy_set in library.enemy_sets.values():
            enemy_set.validate()

        for dungeon in library.dungeons.values():
            dungeon.validate()

    @cached_property
    def standard_encounters(self) -> dict[str, Encounter]:
        encounters = {}
        for id, encounter in self.encounters.items():
            if encounter.encounter_type != EncounterType.SPECIAL:
                encounters[id] = encounter

        return encounters

    @cached_property
    def small_enemies(self) -> dict[str, EnemySet]:
        enemy_sets = {}
        for id, enemy_set in self.enemy_sets.items():
            if (
                enemy_set.set_type != EnemySetType.SPECIAL
                and enemy_set.weight_class == EnemyWeightClass.SMALL
            ):
                enemy_sets[id] = enemy_set

        return enemy_sets

    @cached_property
    def medium_enemies(self) -> dict[str, EnemySet]:
        enemy_sets = {}
        for id, enemy_set in self.enemy_sets.items():
            if (
                enemy_set.set_type != EnemySetType.SPECIAL
                and enemy_set.weight_class == EnemyWeightClass.MEDIUM
            ):
                enemy_sets[id] = enemy_set

        return enemy_sets

    @cached_property
    def large_enemies(self) -> dict[str, EnemySet]:
        enemy_sets = {}
        for id, enemy_set in self.enemy_sets.items():
            if (
                enemy_set.set_type != EnemySetType.SPECIAL
                and enemy_set.weight_class == EnemyWeightClass.LARGE
            ):
                enemy_sets[id] = enemy_set

        return enemy_sets

    @staticmethod
    def get_standard_encounter() -> Encounter:
        library = ContentLibrary.get_library()
        return random.choice(list(library.standard_encounters.values()))
