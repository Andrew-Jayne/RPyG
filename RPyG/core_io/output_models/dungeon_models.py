from dataclasses import dataclass

from RPyG.core_io.output_models.base_models import OutputMessage


@dataclass(kw_only=True, frozen=True, slots=True)
class DungeonStartMessage(OutputMessage):
    dungeon_name: str


@dataclass(kw_only=True, frozen=True, slots=True)
class DungeonUpdateMessage(OutputMessage):
    @dataclass(kw_only=True, frozen=True, slots=True)
    class DungeonEvent:
        message: str

    @dataclass(kw_only=True, frozen=True, slots=True)
    class HealRoomEvent(DungeonEvent):
        message: str

    @dataclass(kw_only=True, frozen=True, slots=True)
    class EmptyTravelEvent(DungeonEvent):
        message: str = ""

    @dataclass(kw_only=True, frozen=True, slots=True)
    class ShortcutEvent(DungeonEvent):
        message: str

    @dataclass(kw_only=True, frozen=True, slots=True)
    class EnemyEncounterEvent(DungeonEvent):
        message: str

    @dataclass(kw_only=True, frozen=True, slots=True)
    class BossEncounterEvent(DungeonEvent):
        message: str

    message: str = ""
    event: DungeonEvent


@dataclass(kw_only=True, frozen=True, slots=True)
class DungeonEndMessage(OutputMessage):
    dungeon_name: str
