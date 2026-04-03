import random
from enum import Enum
from functools import cached_property
from typing import final

from RPyG.constructs import (
    ContentDataDict,
    Dungeon,
    Encounter,
    EncounterEffect,
    EnemyActor,
    EnemySet,
    EnemySetType,
    EnemyWeightClass,
    StoryEvent,
)
from RPyG.constructs.data_types import (
    DungeonDataDict,
    EncounterDataDict,
    EncounterEffectDataDict,
    EnemyDataDict,
    EnemySetDataDict,
    StoryEventDataDict,
)


class ContentKind(Enum):
    EnemySet = "EnemySet"
    Dungeon = "Dungeon"
    Enemy = "Enemy"
    Encounters = "Encounters"
    EncounterEffect = "EncounterEffect"
    StoryEvent = "StoryEvent"


@final
class ContentLibrary:
    enemies: dict[str, EnemyActor]
    enemy_sets: dict[str, EnemySet]
    story_events: dict[str, StoryEvent]
    encounters: dict[str, Encounter]
    encounter_effects: dict[str, EncounterEffect]
    dungeons: dict[str, Dungeon]
    _instance: "ContentLibrary | None" = None

    @staticmethod
    def build_story_events(
        story_events_data: dict[str, StoryEventDataDict],
    ) -> dict[str, StoryEvent]:
        all_events: dict[str, StoryEvent] = {}
        for value in story_events_data.values():
            event = StoryEvent(**value)
            all_events[event.progress_trigger] = event

        return all_events

    @staticmethod
    def build_encounters(
        encounters_data: dict[str, EncounterDataDict],
    ) -> dict[str, Encounter]:
        all_encouters: dict[str, Encounter] = {}
        for key, value in encounters_data.items():
            all_encouters[key] = Encounter(**value)

        return all_encouters

    @staticmethod
    def build_enemy_sets(
        enemy_sets_data: dict[str, EnemySetDataDict],
    ) -> dict[str, EnemySet]:
        all_enemy_sets: dict[str, EnemySet] = {}
        for key, value in enemy_sets_data.items():
            all_enemy_sets[key] = EnemySet(**value)

        return all_enemy_sets

    @staticmethod
    def build_enemies(enemies_data: dict[str, EnemyDataDict]) -> dict[str, EnemyActor]:
        all_enemies: dict[str, EnemyActor] = {}
        for key, value in enemies_data.items():
            all_enemies[key] = EnemyActor(**value)

        return all_enemies

    @staticmethod
    def build_dungeons(dungeons_data: dict[str, DungeonDataDict]) -> dict[str, Dungeon]:
        all_dungeons: dict[str, Dungeon] = {}
        for key, value in dungeons_data.items():
            all_dungeons[key] = Dungeon(**value)

        return all_dungeons

    @staticmethod
    def build_encounter_effects(
        encounter_effects_data: dict[str, EncounterEffectDataDict],
    ) -> dict[str, EncounterEffect]:
        all_encounter_effects: dict[str, EncounterEffect] = {}
        for key, value in encounter_effects_data.items():
            all_encounter_effects[key] = EncounterEffect(**value)

        return all_encounter_effects

    def __init__(self, content_data: dict[str, ContentDataDict]):
        if ContentLibrary._instance is None:
            enemies_data: dict[str, EnemyDataDict] = dict()
            enemy_sets_data: dict[str, EnemySetDataDict] = dict()
            dungeons_data: dict[str, DungeonDataDict] = dict()
            encounters_data: dict[str, EncounterDataDict] = dict()
            story_events_data: dict[str, StoryEventDataDict] = dict()
            encounter_effects_data: dict[str, EncounterEffectDataDict] = dict()

            for item, value in content_data.items():
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

                ## all of the ignores here are because the initialized empty dicts  do not have the expected values
                ## however as items are sorted into them they will get the correct data
                ## these typed dicts are around to help with keeping data data structures clear in this this large data store
                match item_kind:
                    case ContentKind.EnemySet:
                        enemy_sets_data[item] = value  # pyright: ignore[reportArgumentType]
                    case ContentKind.Dungeon:
                        dungeons_data[item] = value  # pyright: ignore[reportArgumentType]
                    case ContentKind.Enemy:
                        enemies_data[item] = value  # pyright: ignore[reportArgumentType]
                    case ContentKind.Encounters:
                        encounters_data[item] = value  # pyright: ignore[reportArgumentType]
                    case ContentKind.StoryEvent:
                        story_events_data[item] = value  # pyright: ignore[reportArgumentType]
                    case ContentKind.EncounterEffect:
                        encounter_effects_data[item] = value  # pyright: ignore[reportArgumentType]
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
        all_dungeons = list(library.dungeons.values())

        dungeon = random.choice(all_dungeons)
        while dungeon.special_dungeon is True:
            dungeon = random.choice(all_dungeons)

        return dungeon
