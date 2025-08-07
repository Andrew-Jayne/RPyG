from dataclasses import dataclass


# Input requests
@dataclass
class InputRequest:
    messages: list[str]


@dataclass
class UserPromptRequest(InputRequest):
    options: list[str]
    messages: list[str]


@dataclass
class CustomTextRequest(InputRequest):
    messages: list[str]
    max_length: int


# Output Messages
@dataclass
class OutputMessage:
    messages: list[str]


@dataclass
class BattleHudMessage:
    messages: list[str]
    combatant_data: dict
