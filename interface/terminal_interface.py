from typing import Any

from RPyG.core_io import RPyGInterface


class BasicTerminalInterface(RPyGInterface):
    input_buffer: dict[str, Any]

    def __init__(self):
        super().__init__()
        self.input_buffer = {}

    def show_ouput(self, request_data: dict) -> None:
        return print(request_data)

    def request_input(self, request_data: dict) -> None:
        self.input_buffer = {"data": input(str(request_data))}

    def receive_input(self) -> dict:
        data = self.input_buffer.get("data")
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_input before calling receive_input"
            )
        # reset buffer
        self.input_buffer = {}
        return data
