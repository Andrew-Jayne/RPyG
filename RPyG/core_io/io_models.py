from dataclasses import dataclass
from enum import Enum

from RPyG.utilities import ensure_type


# Input requests
@dataclass
class InputRequest:
    prompts: list[str]


@dataclass
class UserPromptRequest(InputRequest):
    options: list[str]
    prompts: list[str]


@dataclass
class CustomTextRequest(InputRequest):
    prompts: list[str]
    max_length: int


# Output Messages
class UIElement(Enum):
    BATTLE_HUD = "BATTLE_HUD"
    QUEST_LOG = "QUEST_LOG"


@dataclass
class OutputMessage:
    message: str
    target_element: UIElement = UIElement.QUEST_LOG

    def __post__init__(self) -> None:
        ensure_type(self.message, str, "output_message")
        ensure_type(self.target_element, UIElement, "target_element")


@dataclass
class CombatantData:
    stuff: str


@dataclass(kw_only=True)
class BattleHudMessage(OutputMessage):
    message: str
    combatant_data: CombatantData
    target_element: UIElement = UIElement.BATTLE_HUD


@dataclass(kw_only=True)
class EmptyDistanceMessage(OutputMessage):
    distance: int
    message: str = ""
    target_element: UIElement = UIElement.QUEST_LOG
