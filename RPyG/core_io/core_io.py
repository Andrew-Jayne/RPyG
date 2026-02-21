from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Self, final

from RPyG.core_io.io_models import InputRequest, OutputMessage
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.game_state import GameState


class RPyGInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def show_ouput(self, output: OutputMessage) -> None:
        pass

    @abstractmethod
    def request_input(self, request: InputRequest) -> None:
        pass

    @abstractmethod
    def receive_input(self) -> str:
        pass

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

    def request_input(self, request: InputRequest) -> None:
        return self.interface.request_input(request)

    def receive_input(self) -> str:
        return self.interface.receive_input()

    def send_output(self, output: OutputMessage) -> None:
        return self.interface.show_ouput(output)

    def validate(self) -> None:
        ## this should have some kind of round trip test or something
        return
