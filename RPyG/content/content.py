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
    EncounterEffect,
    EnemySet,
    EnemySetType,
    EnemyWeightClass,
    StoryEvent,
)
from RPyG.utilities import ensure_type


class ContentKind(Enum):
    EnemySet = "EnemySet"
    Dungeon = "Dungeon"
    Enemy = "Enemy"
    Encounters = "Encounters"
    EncounterEffect = "EncounterEffect"
    StoryEvent = "StoryEvent"


class ContentLibrary:
    enemies: dict[str, Enemy]
    enemy_sets: dict[str, EnemySet]
    story_events: dict[str, StoryEvent]
    encounters: dict[str, Encounter]
    encounter_effects: dict[str, EncounterEffect]
    dungeons: dict[str, Dungeon]
    _instance: "ContentLibrary | None" = None

    @staticmethod
    def build_story_events(story_events_data: dict[str, Any]) -> dict[str, StoryEvent]:  # pyright: ignore[reportExplicitAny]
        all_events: dict[str, StoryEvent] = {}
        for value in story_events_data.values():
            event = StoryEvent(**value)
            all_events[event.progress_trigger] = event

        return all_events

    @staticmethod
    def build_encounters(encounters_data: dict[str, Any]) -> dict[str, Encounter]:  # pyright: ignore[reportExplicitAny]
        all_encouters: dict[str, Encounter] = {}
        for key, value in encounters_data.items():
            all_encouters[key] = Encounter(**value)

        return all_encouters

    @staticmethod
    def build_enemy_sets(enemy_sets_data: dict[str, Any]) -> dict[str, EnemySet]:  # pyright: ignore[reportExplicitAny]
        all_enemy_sets: dict[str, EnemySet] = {}
        for key, value in enemy_sets_data.items():
            all_enemy_sets[key] = EnemySet(**value)

        return all_enemy_sets

    @staticmethod
    def build_enemies(enemies_data: dict[str, Any]) -> dict[str, Enemy]:  # pyright: ignore[reportExplicitAny]
        all_enemies: dict[str, Enemy] = {}
        for key, value in enemies_data.items():
            all_enemies[key] = Enemy(**value)

        return all_enemies

    @staticmethod
    def build_dungeons(dungeons_data: dict[str, Any]) -> dict[str, Dungeon]:  # pyright: ignore[reportExplicitAny]
        all_dungeons: dict[str, Dungeon] = {}
        for key, value in dungeons_data.items():
            all_dungeons[key] = Dungeon(**value)

        return all_dungeons

    @staticmethod
    def build_encounter_effects(
        encounter_effects_data: dict[str, Any],  # pyright: ignore[reportExplicitAny]
    ) -> dict[str, EncounterEffect]:
        all_encounter_effects: dict[str, EncounterEffect] = {}
        for key, value in encounter_effects_data.items():
            all_encounter_effects[key] = EncounterEffect(**value)

        return all_encounter_effects

    @staticmethod
    def load_content_files(dir_path: str) -> dict[str, dict[str, Any]]:  # pyright: ignore[reportExplicitAny]
        """
        Load all JSON files in the given directory and merge their contents into a single dictionary.
        """
        ensure_type(dir_path, str, "dir_path")
        combined_content: dict[str, dict[str, Any]] = {}  # pyright: ignore[reportExplicitAny]

        # Walk through the directory and look for JSON files
        for root, _dirs, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_extension = os.path.splitext(file_path)[1]
                content_object: dict[str, dict[str, Any]] = {}  # pyright: ignore[reportExplicitAny]
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

            enemies_data: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]
            enemy_sets_data: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]
            dungeons_data: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]
            encounters_data: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]
            story_events_data: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]
            encounter_effects_data: dict[str, Any] = {}  # pyright: ignore[reportExplicitAny]

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
                    case ContentKind.EncounterEffect:
                        encounter_effects_data[item] = value
                    case _:  # pyright: ignore[reportUnnecessaryComparison]
                        raise ValueError(  # pyright: ignore[reportUnreachable]
                            f"item {item} has unsupported kind {item_kind}"
                        )

            self.story_events = ContentLibrary.build_story_events(story_events_data)
            self.encounters = ContentLibrary.build_encounters(encounters_data)
            self.enemies = ContentLibrary.build_enemies(enemies_data)
            self.enemy_sets = ContentLibrary.build_enemy_sets(enemy_sets_data)
            self.dungeons = ContentLibrary.build_dungeons(dungeons_data)
            self.encounter_effects = ContentLibrary.build_encounter_effects(
                encounter_effects_data
            )

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
        for event_id, story_event in library.story_events.items():
            if story_event.validate() is False:
                raise RuntimeError(f"{event_id} failed to validate")

        for encounter_id, encounter in library.encounters.items():
            if encounter.validate() is False:
                raise RuntimeError(f"{encounter_id} failed to validate")

        for enemy_id, enemy in library.enemies.items():
            if enemy.validate() is False:
                raise RuntimeError(f"{enemy_id} failed to validate")

        for enemy_set_id, enemy_set in library.enemy_sets.items():
            if enemy_set.validate() is False:
                raise RuntimeError(f"{enemy_set_id} failed to validate")

        for dungeon_id, dungeon in library.dungeons.items():
            if dungeon.validate() is False:
                raise RuntimeError(f"{dungeon_id} failed to validate")

        for effect_id, effect in library.encounter_effects.items():
            if effect.validate() is False:
                raise RuntimeError(f"{effect_id} failed to validate")

    @cached_property
    def standard_encounters(self) -> dict[str, Encounter]:
        encounters: dict[str, Encounter] = {}
        for id, encounter in self.encounters.items():
            if encounter.special_encounter is False:
                encounters[id] = encounter

        return encounters

    @cached_property
    def small_enemies(self) -> dict[str, EnemySet]:
        enemy_sets: dict[str, EnemySet] = {}
        for id, enemy_set in self.enemy_sets.items():
            if (
                enemy_set.set_type != EnemySetType.SPECIAL
                and enemy_set.weight_class == EnemyWeightClass.SMALL
            ):
                enemy_sets[id] = enemy_set

        return enemy_sets

    @cached_property
    def medium_enemies(self) -> dict[str, EnemySet]:
        enemy_sets: dict[str, EnemySet] = {}
        for id, enemy_set in self.enemy_sets.items():
            if (
                enemy_set.set_type != EnemySetType.SPECIAL
                and enemy_set.weight_class == EnemyWeightClass.MEDIUM
            ):
                enemy_sets[id] = enemy_set

        return enemy_sets

    @cached_property
    def large_enemies(self) -> dict[str, EnemySet]:
        enemy_sets: dict[str, EnemySet] = {}
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

    @staticmethod
    def get_standard_dungeon() -> Dungeon:
        library = ContentLibrary.get_library()
        return random.choice(list(library.dungeons.values()))
