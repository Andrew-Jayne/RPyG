from dataclasses import dataclass

from RPyG.utilities import ensure_type


# Input requests
@dataclass
class InputRequest:
    prompts: list[str]


@dataclass
class UserPromptRequest(InputRequest):
    # Barf this needs to be better
    options: list[str] | list[str | None]
    prompts: list[str]
    show_options: bool = True


@dataclass
class CustomTextRequest(InputRequest):
    prompts: list[str]
    max_length: int


@dataclass
class OutputMessage:
    message: str
    line_delay: float = 1.0
    reset_display: bool = False

    def __post__init__(self) -> None:
        ensure_type(self.message, str, "output_message")
        ensure_type(self.line_delay, float, "line_delay")


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
