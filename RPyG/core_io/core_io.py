from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self, final

from RPyG.core_io import input_models, output_models
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
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
    def get_content_data(self) -> dict[str, dict[str, Any]]:  # pyright: ignore[reportExplicitAny]
        pass

    @abstractmethod
    def get_game_state(self) -> "GameState":
        pass

    @abstractmethod
    def save_game_state(self, game_state: "GameState") -> None:
        pass


@final
class CoreIO:
    _instance: Self | None = None
    interface: RPyGInterface

    def __init__(self, interface: RPyGInterface):
        ensure_type(interface, RPyGInterface, "interface")
        if CoreIO._instance is None:
            self.interface = interface
            CoreIO._instance = self
        else:
            raise RuntimeError("CoreIO already initialized")

    @classmethod
    def get_core_io(cls) -> "CoreIO":
        if CoreIO._instance is not None:
            return CoreIO._instance
        else:
            raise RuntimeError(
                "Attempted to acess CoreIO instance before initialization"
            )

    def request_input(self, request: input_models.InputRequest) -> None:
        return self.interface.request_input(request)

    def receive_input(self) -> str:
        return self.interface.receive_input()

    def send_output(self, output: output_models.OutputMessage) -> None:
        return self.interface.show_ouput(output)

    def validate(self) -> None:
        ## this should have some kind of round trip test or something
        return
