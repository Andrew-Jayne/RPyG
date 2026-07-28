from dataclasses import dataclass

from RPyG.core_io.output_models.actor_models import (
    ActorDefeatedMessage,
    HealthUpdateMessage,
    UseGoldMessage,
    UsePotionMessage,
)
from RPyG.core_io.output_models.base_models import OutputMessage
from RPyG.core_io.output_models.combat_models import (
    BattleEndMessage,
    BattleHudData,
    BattleStartMessage,
    BattleUpdateMessage,
)
from RPyG.core_io.output_models.dungeon_models import (
    DungeonEndMessage,
    DungeonStartMessage,
    DungeonUpdateMessage,
)
from RPyG.core_io.output_models.encounter_models import (
    EnemyEncounterMessage,
    FleeResultMessage,
    GenericEncounterMessage,
    MerchantInteractionMessage,
    MerchantMenuHudDataMessage,
)
from RPyG.core_io.output_models.story_models import GenericStoryMessage
from RPyG.utilities import ensure_type


## homeless models for now
@dataclass(kw_only=True, frozen=True, slots=True)
class EmptyDistanceMessage(OutputMessage):
    distance: int
    message: str = ""

    def __post_init__(self) -> None:
        ensure_type(self.distance, int, "distance")
        ensure_type(self.message, str, "message")


@dataclass(kw_only=True, frozen=True, slots=True)
class EventAfterEmptyMessage(OutputMessage):
    distance: int
    message: str = ""


@dataclass(kw_only=True, frozen=True, slots=True)
class GameEndMessage(OutputMessage):
    message: str = ""
    success: bool
    post_game_recap: str


__all__ = [
    "ActorDefeatedMessage",
    "OutputMessage",
    "BattleEndMessage",
    "BattleHudData",
    "FleeResultMessage",
    "UseGoldMessage",
    "EnemyEncounterMessage",
    "BattleStartMessage",
    "BattleUpdateMessage",
    "DungeonEndMessage",
    "DungeonStartMessage",
    "DungeonUpdateMessage",
    "EmptyDistanceMessage",
    "GameEndMessage",
    "EventAfterEmptyMessage",
    "UsePotionMessage",
    "HealthUpdateMessage",
    "GenericEncounterMessage",
    "GenericStoryMessage",
    "MerchantMenuHudDataMessage",
    "MerchantInteractionMessage",
]
