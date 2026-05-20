import os
import textwrap
import time
from typing import override

from interfaces.interface_components import (
    ContentFileLoaderSource,
    JsonGameStateHandler,
)
from RPyG.constructs import ContentDataDict, PlayableActor, PlayerParty
from RPyG.core_io import CoreIO, RPyGInterface, input_models, output_models
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state import GameState
from RPyG.utilities import ensure_type, setup_logger


welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----

             NOTE: All Prompts in this game are case insensitive

"""

logger = setup_logger(__name__)


class BasicTerminalInterface(RPyGInterface):
    __slots__: tuple[str, ...] = ("string_buffer", "integer_buffer")
    string_buffer: str | None
    integer_buffer: int | None

    def __init__(self):
        RPyGInterface.__init__(self)
        self.string_buffer = None
        self.integer_buffer = None
        self.show_output(output_models.OutputMessage(message=welcome_message))

    @override
    def get_content_data(self) -> dict[str, ContentDataDict]:
        return ContentFileLoaderSource.get_content()

    @override
    def save_game_state(self, game_state: GameState) -> None:
        JsonGameStateHandler.save_game_state(game_state)

    @override
    def show_output(self, output: output_models.OutputMessage) -> None:
        ending = "\n"
        wrapped_message = ""

        # Split the message into lines to handle them individually
        lines = output.message.split("\n")
        for line in lines:
            # Apply text wrapping to each line individually
            wrapped_line = textwrap.fill(line, width=80)
            wrapped_message += wrapped_line + "\n"

        # Print the final wrapped message, removing the last added newline and adding the custom ending
        time.sleep(1)
        print(wrapped_message.rstrip("\n"), end=ending)

    @override
    def request_str_input(self, request: input_models.InputRequest) -> None:
        ensure_type(request, input_models.InputRequest, "request")
        match request:
            case input_models.UserPromptRequest():
                content = self.prompt_user(
                    options=request.options,
                    prompts=request.prompts,
                )

            case input_models.CustomTextRequest():
                content = self.custom_text_entry(
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
                content = self.prompt_user(
                    options=request.options,
                    prompts=request.prompts,
                )

            case input_models.CustomTextRequest():
                content = self.custom_text_entry(
                    request.prompts,
                    request.max_length,
                )
            case _:
                raise ValueError(
                    f"Got Unknown Child class of input_models.InputRequest {type(request).__name__}"
                )

        if self.integer_buffer is not None:
            raise RuntimeError(
                "Input Buffer is not empty, receive_input() must be called to empty buffer"
            )
        self.integer_buffer = int(content)

    @override
    def receive_str_input(self) -> str:
        data = self.string_buffer
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_input() before calling receive_input()?"
            )
        # reset buffer
        self.string_buffer = None
        return data

    @override
    def receive_int_input(self) -> int:
        data = self.integer_buffer
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_input() before calling receive_input()?"
            )
        # reset buffer
        self.integer_buffer = None
        return data

    @override
    def get_game_state(self) -> "GameState":
        logger.info("Getting Start type")
        start_type = self.get_start_type()
        match start_type:
            case "LOAD":
                game_state = JsonGameStateHandler.load_game_state()
            case "NEW":
                game_state = self.party_start()
            case "USE_DEFAULT":
                game_state = GameState.build(self.default_party())
            case _:
                raise ValueError("Invalid Game Start Type")

        logger.info("starting game with %s start type", start_type)

        return game_state

    @staticmethod
    def clear_display() -> None:
        # For Windows
        if os.name == "nt":
            os.system("cls")  # pyright: ignore[reportUnusedCallResult]
        # For macOS and Linux
        else:
            os.system('clear && printf "\\e[3J"')  # pyright: ignore[reportUnusedCallResult]

    @staticmethod
    def sanitize(
        input_string: str,
        *,
        max_length: int = 32,
    ) -> str:
        """
        This function Sanitizes strings passed into it and returns up to the max length chars (Default is 32)
        With most escape sequences and control chars removed

        Will raise ValueError if a string exceeding 512 chars is passed
        """
        # raise ValueError if string is longer than 512 Chars
        if len(input_string) > 512:
            raise ValueError("Input Length Exceeds Expected Parameters: Exiting!")
        # Set unwanted chars
        chars_to_remove = (
            r"!#*"  # Basic symbols
            r".[]{}"  # Brackets
            r"\\|\":;"  # Escaped stuff
            r"/<>\\()"  # Slashes and parens
            r"'"  # Final single quote
        )
        control_chars = "".join(map(chr, range(0, 32))) + chr(127)
        literal_control_strings = [
            "\\n",
            "\\t",
            "\\r",
            "\\x0c",
            "\\x0b",
        ]  # Literal string representations of control chars
        # Remove unwanted chars
        limited_string = input_string[
            :max_length
        ]  # Limit the input to the desired length
        for literal in literal_control_strings:
            limited_string = limited_string.replace(literal, "")
        cleaned_string = ""
        for char in limited_string:
            if char not in chars_to_remove and char not in control_chars:
                cleaned_string += char

        return cleaned_string

    def validate_input(self, choice_list: list[str]) -> str:
        """
        Checks that the string input by the user is in the allowed list of responses
        Sanitizes the input then returns up to the max length specified
        """
        options_list = "\n".join(choice_list) + "\n"
        chosen_action = ""
        dumb_check = 0
        while chosen_action not in choice_list:
            chosen_action = self.sanitize(input("").upper())
            if chosen_action not in choice_list:
                self.show_output(
                    output_models.OutputMessage(
                        message=f"That is not a Valid Option. Try again, valid options are \n{options_list}"
                    )
                )
                dumb_check += 1
                if dumb_check == 10:
                    raise ValueError(
                        "Look it's not hard, just enter a valid choice...."
                    )
        return chosen_action

    def custom_text_entry(
        self,
        input_messages: list[str],
        max_length: int,
    ) -> str:
        self.show_output(output_models.OutputMessage(message="\n".join(input_messages)))
        return self.sanitize(input()[:max_length])

    def prompt_user(
        self,
        options: list[str],
        prompts: list[str],
    ) -> str:
        ensure_type(options, list, "options")
        ensure_type(prompts, list, "prompts")

        formatted_message = ""
        for message in prompts:
            formatted_message += f"{message}\n"
        formatted_message += "\n"

        for option in options:
            formatted_message += f"{option}\n"

        formatted_message += "\n"

        self.show_output(output_models.OutputMessage(message=formatted_message))

        response = self.validate_input(options)
        return response

    @staticmethod
    def default_party() -> PlayerParty:
        party_members: list[PlayableActor] = []
        default_names = ("Conan", "Merlin", "Robin")
        default_specialization = ("WARRIOR", "MAGE", "ROGUE")
        for index in range(0, 3):
            party_members.append(
                PlayableActor.build(
                    default_names[index],
                    default_specialization[index],
                )
            )

        return PlayerParty(
            members=party_members,
            name="The Default Party",
        )

    @staticmethod
    def get_start_type() -> str:
        match os.path.exists("savegame.rpygs"):
            case True:
                start_game_options = ["NEW", "LOAD"]
                start_game_messages = [
                    "Would you like to Start a new game or Load an existing save?",
                    "Options are:",
                ]
            case False:
                start_game_options = ["NEW", "USE_DEFAULT"]
                start_game_messages = [
                    "Type 'NEW' to start a new game",
                    "You will be able to save your game later and load it here",
                    "Type 'USE_DEFAULT' to start a new game with the default party",
                    "Options are:",
                ]
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(  # pyright: ignore[reportUnreachable]
                    "os.path.exists('savegame.rpygs') did not return a bool and something is very wrong"
                )

        core_io = CoreIO.get_core_io()
        core_io.send_output(
            output_models.OutputMessage(
                message="Welcome to RPyG, a text based RPG in Python"
            )
        )
        core_io.request_str_input(
            input_models.UserPromptRequest(
                options=start_game_options,
                prompts=start_game_messages,
            )
        )
        player_action = core_io.receive_str_input()
        return player_action

    @staticmethod
    def party_start() -> GameState:
        party_size_choices = ["1", "2", "3"]
        party_size_messages = ["How many members are in your party?"]

        specialization_choices = ["WARRIOR", "MAGE", "ROGUE"]
        specialization_messages = ["What Specialization will this member use?"]

        member_name_messages = [
            "Before their journey can begin you must name your Character",
            "NOTE: Case is respected but names longer than 32 characters will be truncated",
        ]

        party_name_messages = [
            "Before their journey can begin you must name your Party",
            "NOTE: Case is respected but names longer than 64 characters will be truncated",
        ]
        core_io = CoreIO.get_core_io()

        core_io.request_int_input(
            input_models.UserPromptRequest(
                options=party_size_choices,
                prompts=party_size_messages,
            )
        )
        party_size = core_io.receive_int_input()

        party_instances: list[PlayableActor] = []
        for _ in range(0, party_size):
            core_io = CoreIO.get_core_io()
            core_io.request_str_input(
                input_models.CustomTextRequest(
                    prompts=member_name_messages,
                    max_length=32,
                )
            )
            member_name = core_io.receive_str_input()
            core_io.request_str_input(
                input_models.UserPromptRequest(
                    prompts=specialization_messages,
                    options=specialization_choices,
                )
            )
            member_specialization = core_io.receive_str_input()
            member = PlayableActor.build(member_name, member_specialization)
            party_instances.append(member)

        core_io.request_str_input(
            input_models.CustomTextRequest(
                prompts=party_name_messages,
                max_length=64,
            )
        )
        party_name = core_io.receive_str_input()

        return GameState.build(PlayerParty(party_name, party_instances))
