from typing import TYPE_CHECKING, Self, final

from RPyG.core_io import input_models, output_models
from RPyG.utilities import ensure_type


if TYPE_CHECKING is True:
    from RPyG.core_io.rpyg_interface import RPyGInterface


@final
class CoreIO:
    __slots__: tuple[str, ...] = ("interface",)
    _instance: Self | None = None
    interface: RPyGInterface

    def __init__(self, interface: RPyGInterface):
        from RPyG.core_io import RPyGInterface

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

    def request_str_input(self, request: input_models.InputRequest) -> None:
        return self.interface.request_str_input(request)

    def request_int_input(self, request: input_models.InputRequest) -> None:
        return self.interface.request_int_input(request)

    def receive_str_input(self) -> str:
        return self.interface.receive_str_input()

    def receive_int_input(self) -> int:
        return self.interface.receive_int_input()

    def send_output(self, output: output_models.OutputMessage) -> None:
        return self.interface.show_ouput(output)

    def validate(self) -> None:
        ## this should have some kind of round trip test or something
        return
