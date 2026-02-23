from dataclasses import dataclass

from RPyG.utilities import ensure_type


@dataclass
class OutputMessage:
    message: str
    line_delay: float = 1.0
    reset_display: bool = False

    def __post_init__(self) -> None:
        ensure_type(self.message, str, "output_message")
        ensure_type(self.line_delay, float, "line_delay")
        ensure_type(self.reset_display, bool, "reset_display")


# @dataclass
# class CombatantData:
#     stuff: str


@dataclass
class BattleState:
    data: dict[str, str]


@dataclass
class BattleEvent:
    data: dict[str, str]


@dataclass(kw_only=True)
class BattleHudMessage(OutputMessage):
    message: str
    # combatant_data: CombatantData


@dataclass(kw_only=True)
class EmptyDistanceMessage(OutputMessage):
    distance: int
    message: str = ""

    def __post_init__(self) -> None:
        ensure_type(self.distance, int, "distance")
        ensure_type(self.message, str, "message")
