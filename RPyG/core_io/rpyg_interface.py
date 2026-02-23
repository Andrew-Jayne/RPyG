from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from RPyG.core_io import input_models, output_models


if TYPE_CHECKING is True:
    from RPyG.constructs import ContentDataDict
    from RPyG.game_state import GameState


class RPyGInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def show_ouput(self, output: output_models.OutputMessage) -> None:
        pass

    @abstractmethod
    def request_input(self, request: input_models.InputRequest) -> None:
        pass

    @abstractmethod
    def receive_input(self) -> str:
        pass

    # Needs the big ass typed dict thing
    @abstractmethod
    def get_content_data(self) -> dict[str, ContentDataDict]:
        pass

    @abstractmethod
    def get_game_state(self) -> "GameState":
        pass

    @abstractmethod
    def save_game_state(self, game_state: "GameState") -> None:
        pass
