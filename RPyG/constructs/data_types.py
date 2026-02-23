"""
A collection of TypedDicts to represent the structure of items
used in the initialzation of the content library
these are typed dicts not constructs, and should not be confused
with the equivilant functional objects found in RPyG.constructs
"""

from typing import TypedDict


class SceneDataDict(TypedDict):
    kind: str
    length: int
    encounter_id: str | None
    dungeon_id: str | None
    story_event_id: str | None


class GlobalSceneDataDict(TypedDict):
    kind: str
    length: int


class EncounterDataDict(TypedDict):
    kind: str
    primary_encounter: bool
    special_encounter: bool
    prompts: list[str]
    success_choice: str | None
    retry_choice: str | None
    failure_choice: str | None
    success_effects: list[str]
    retry_effects: list[str]
    failure_effects: list[str]
    success_messages: list[str]
    retry_messages: list[str]
    failure_messages: list[str]


class EncounterEffectDataDict(TypedDict):
    kind: str
    actor_action: str
    targets: str
    magnitude: int
    effect_messages: list[str]
    extra_effects: list[str]


class DungeonDataDict(TypedDict):
    kind: str
    name: str
    length: int
    boss_enemy_id: str
    enemy_set_id: str
    start_message: str
    shortcut_message: str
    heal_room_message: str
    boss_encounter_message: str


class EnemySetDataDict(TypedDict):
    kind: str
    plural_name: str
    group_name: str
    weight_class: str
    set_type: str
    enemy_ids: list[str]


class EnemyDataDict(TypedDict):
    kind: str
    variant_grade: str
    name: str
    health: int
    strength: int
    intellect: int
    agility: int
    luck: int
    attack_name: str
    is_special: bool


class StoryEventDataDict(TypedDict):
    kind: str
    progress_trigger: int
    event_type: str
    encounter_id: str
    messages: list[str]
    success_messages: list[str]
    failure_messages: list[str]


ContentDataDict = (
    DungeonDataDict
    | EncounterDataDict
    | EncounterEffectDataDict
    | EnemyDataDict
    | EnemySetDataDict
    | GlobalSceneDataDict
    | SceneDataDict
    | StoryEventDataDict
)
