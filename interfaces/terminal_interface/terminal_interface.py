import textwrap
import time
from typing import final, override

from RPyG.constructs import ContentDataDict
from RPyG.core_io import RPyGInterface, input_models, output_models
from RPyG.game_state import GameState
from RPyG.utilities import ensure_type, setup_logger

from ..interface_components import (
    ContentFileLoaderSource,
    JsonGameStateHandler,
)
from . import text_strings
from .output_sorter import output_message
from .utils import (
    custom_text_entry,
    default_party,
    get_start_type,
    party_start,
    prompt_user,
)


logger = setup_logger(__name__)


@final
class BasicTerminalInterface(RPyGInterface):
    __slots__: tuple[str, ...] = (
        "string_buffer",
        "integer_buffer",
        "game_state_handler",
    )
    string_buffer: str | None
    integer_buffer: int | None
    game_state_handler: JsonGameStateHandler

    def __init__(self):
        RPyGInterface.__init__(self)
        self.string_buffer = None
        self.integer_buffer = None
        self.game_state_handler = JsonGameStateHandler()
        self.show_output(
            output_models.OutputMessage(message=text_strings.welcome_message)
        )

    @override
    def get_content_data(self) -> dict[str, ContentDataDict]:
        return ContentFileLoaderSource.get_content()

    @override
    def save_game_state(self, game_state: GameState) -> None:
        self.game_state_handler.save_game_state(game_state)

    @override
    def get_game_state(self) -> GameState:
        logger.info("Getting Start type")
        start_type = get_start_type()
        match start_type:
            case "LOAD":
                game_state = self.game_state_handler.load_game_state()
            case "NEW":
                game_state = party_start()
            case "USE_DEFAULT":
                game_state = GameState.build(default_party())
            case _:
                raise ValueError("Invalid Game Start Type")

        logger.info("starting game with %s start type", start_type)

        return game_state

    @override
    def show_output(self, output: output_models.OutputMessage) -> None:
        ending = "\n"
        wrapped_message = ""

        # Split the message into lines to handle them individually
        lines = output_message(output).split("\n")
        for line in lines:
            # Apply text wrapping to each line individually
            wrapped_message += textwrap.fill(line, width=80) + "\n"

        # Print the final wrapped message, removing the last added newline and adding the custom ending
        time.sleep(1)
        print(wrapped_message.rstrip("\n"), end=ending)

    @override
    def request_str_input(self, request: input_models.InputRequest) -> None:
        ensure_type(request, input_models.InputRequest, "request")
        match request:
            case input_models.UserPromptRequest():
                content = str(
                    prompt_user(
                        options=request.options,
                        prompts=request.prompts,
                    )
                )

            case input_models.CustomTextRequest():
                content = custom_text_entry(
                    request.prompts,
                    request.max_length,
                )
            case _:
                raise ValueError(
                    f"Got Unknown Child class of input_models.InputRequest {type(request).__name__}"
                )

        if self.string_buffer is not None:
            raise RuntimeError(
                "Input Buffer is not empty, receive_input() must be called to empty buffer"
            )

        self.string_buffer = content

    @override
    def request_int_input(self, request: input_models.InputRequest) -> None:
        ensure_type(request, input_models.InputRequest, "request")
        match request:
            case input_models.UserPromptRequest():
                content = int(
                    prompt_user(
                        options=request.options,
                        prompts=request.prompts,
                        return_index=True,
                    )
                )

            case input_models.CustomTextRequest():
                raise ValueError(
                    "CustomTextRequest is incompatible with request_int_input"
                )

            case _:
                raise ValueError(
                    f"Got Unknown Child class of input_models.InputRequest {type(request).__name__}"
                )

        if self.integer_buffer is not None:
            raise RuntimeError(
                "Input Buffer is not empty, receive_input() must be called to empty buffer"
            )
        self.integer_buffer = content

    @override
    def receive_str_input(self) -> str:
        data = self.string_buffer
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_str_input() before calling receive_input()?"
            )
        # reset buffer
        self.string_buffer = None
        return data

    @override
    def receive_int_input(self) -> int:
        data = self.integer_buffer
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_int_input() before calling receive_input()?"
            )
        # reset buffer
        self.integer_buffer = None
        return data
