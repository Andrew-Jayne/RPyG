from abc import ABC, abstractmethod

from RPyG.game_state import GameState


class GameStateHandler(ABC):
    @staticmethod
    @abstractmethod
    def load_game_state() -> GameState:
        pass

    @staticmethod
    @abstractmethod
    def save_game_state(game_state: GameState) -> None:
        pass
