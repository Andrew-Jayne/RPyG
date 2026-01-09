from abc import ABC, abstractmethod
from typing import Self

from RPyG.core_io.io_models import InputRequest, OutputMessage
from RPyG.utilities import ensure_type


class RPyGInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def show_ouput(self, output: OutputMessage) -> None:
        pass

    @abstractmethod
    def request_input(self, request: InputRequest) -> None:
        pass

    def receive_input(self) -> str:  # pyright: ignore[reportReturnType]
        pass


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
