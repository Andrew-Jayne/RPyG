import hashlib
import hmac
import json
import os
import pickle
import sys
import textwrap
import time
import tomllib
from typing import Any, override

from RPyG import (
    CustomTextRequest,
    InputRequest,
    OutputMessage,
    RPyGInterface,
    UserPromptRequest,
)
from RPyG.actors import PlayableActor, PlayerParty
from RPyG.core_io import CoreIO
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state import GameState
from RPyG.utilities import ensure_type, setup_logger


CONTENT_PATH = "game_content"

# """Secret""" key for HMAC, if you break your file that's on you
secret_key = b"I_WILL_HACK_MY_SAVE_FILE_AND_PROBLEMS_WILL_BE_MY_FAULT"


welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----

             NOTE: All Prompts in this game are case insensitive

"""

logger = setup_logger(__name__)


class BasicTerminalInterface(RPyGInterface):
    input_buffer: str | None

    def __init__(self):
        RPyGInterface.__init__(self)
        self.input_buffer = ""
        self.show_ouput(OutputMessage(welcome_message, line_delay=0))

    @override
    def show_ouput(self, output: OutputMessage) -> None:
        ending = "\n"
        wrapped_message = ""

        # Split the message into lines to handle them individually
        lines = output.message.split("\n")
        for line in lines:
            # Apply text wrapping to each line individually
            wrapped_line = textwrap.fill(line, width=80)
            wrapped_message += wrapped_line + "\n"

        # Print the final wrapped message, removing the last added newline and adding the custom ending
        # Sleep before print based on line delay
        if output.reset_display is True:
            self.clear_display()
        time.sleep(output.line_delay)
        print(wrapped_message.rstrip("\n"), end=ending)

    @override
    def request_input(self, request: InputRequest) -> None:
        ensure_type(request, InputRequest, "request")
        match request:
            case UserPromptRequest():
                displayable_options: list[str] = []
                for item in request.options:
                    if item is not None:
                        displayable_options.append(item)
                content = self.prompt_user(
                    options=displayable_options,
                    prompts=request.prompts,
                    show_options=request.show_options,
                )

            case CustomTextRequest():
                content = self.custom_text_entry(
                    request.prompts,
                    request.max_length,
                )
            case _:
                raise ValueError(
                    f"Got Unknown Child class of InputRequest {type(request).__name__}"
                )

        if self.input_buffer is None:
            raise RuntimeError(
                "Input Buffer is not empty, receive_input() must be called to empty buffer"
            )
        self.input_buffer = content

    @override
    def receive_input(self) -> str:
        data = self.input_buffer
        if data is None:
            raise RuntimeError(
                "Input buffer is empty, did you call request_input() before calling receive_input()?"
            )
        # reset buffer
        self.input_buffer = None
        return data

    @override
    def get_content_data(self) -> dict[str, dict[str, Any]]:  # pyright: ignore[reportExplicitAny]
        """
        Load all JSON files in the given directory and merge their contents into a single dictionary.
        """
        dir_path = CONTENT_PATH
        combined_content: dict[str, dict[str, Any]] = {}  # pyright: ignore[reportExplicitAny]

        # Walk through the directory and look for JSON files
        for root, _dirs, files in os.walk(dir_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_extension = os.path.splitext(file_path)[1]
                content_object: dict[str, dict[str, Any]] = {}  # pyright: ignore[reportExplicitAny]
                match file_extension:
                    case ".json":
                        with open(file_path, "r") as json_file:
                            content_object = json.load(json_file)
                    case ".toml":
                        with open(file_path, "rb") as toml_file:
                            content_object = tomllib.load(toml_file)
                    case _:
                        pass

                new_object = set(content_object.keys())
                all_content = set(combined_content.keys())
                conflicts = new_object.intersection(all_content)
                if conflicts == set():
                    combined_content.update(content_object)
                else:
                    raise ValueError(
                        f"Duplicate Key Declaration found while processing {file_path} conflicting keys {conflicts}"
                    )

        return combined_content

    @override
    def get_game_state(self) -> "GameState":
        logger.info("Getting Start type")
        start_type = self.get_start_type()
        match start_type:
            case "LOAD":
                game_state = self.load_game()
            case "NEW":
                game_state = self.party_start()
            case "USE_DEFAULT":
                game_state = GameState(self.default_party())
            case _:
                raise ValueError("Invalid Game Start Type")

        logger.info("starting game with %s start type", start_type)

        return game_state

    @override
    def save_game_state(self, game_state: GameState) -> None:
        """
        Call this to Save the current state of the player party object to a pickle file then exits the program
        This serves to save all progress of the party
        """

        ensure_type(game_state, GameState, "game_state")

        serialized_data = pickle.dumps(game_state)
        signature = hmac.new(secret_key, serialized_data, hashlib.sha256).digest()

        with open("savegame.rpygs", "wb") as save_file:
            save_file.write(signature + serialized_data)  # pyright: ignore[reportUnusedCallResult]

        core_io = CoreIO.get_core_io()
        core_io.send_output(
            OutputMessage(f"Successfully Saved Game for {game_state.player_party.name}")
        )

        core_io.request_input(
            UserPromptRequest(
                options=["YES", "NO"],
                prompts=["Would you like to keep playing?"],
            )
        )
        match core_io.receive_input():
            case "YES":
                core_io.send_output(
                    OutputMessage("The adventure continues!", reset_display=True)
                )
            case "NO":
                sys.exit(0)
            case _:
                raise ValueError("Must be a choice of 'YES' or 'NO'")

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
        cleaned_string = "".join(
            char
            for char in limited_string
            if char not in chars_to_remove and char not in control_chars
        )

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
                self.show_ouput(
                    OutputMessage(
                        f"That is not a Valid Option. Try again, valid options are \n{options_list}"
                    )
                )
                dumb_check += 1
                if dumb_check == 10:
                    raise FileNotFoundError(
                        "Look it's not hard, just enter a valid choice...."
                    )
        return chosen_action

    def custom_text_entry(
        self,
        input_messages: list[str],
        max_length: int,
    ) -> str:
        self.show_ouput(OutputMessage("\n".join(input_messages)))
        return self.sanitize(input()[:max_length])

    def prompt_user(
        self,
        options: list[str],
        prompts: list[str],
        *,
        show_options: bool = True,
    ) -> str:
        ensure_type(options, list, "options")
        ensure_type(prompts, list, "base_messages")

        formatted_message = ""
        for message in prompts:
            formatted_message += f"{message}\n"
        formatted_message += "\n"

        if show_options is True:
            for option in options:
                formatted_message += f"{option}\n"

        formatted_message += "\n"

        self.show_ouput(OutputMessage(formatted_message))

        response = self.validate_input(options)
        return response

    @staticmethod
    def default_party() -> PlayerParty:
        party_members: list[PlayableActor] = []
        default_names = ("Conan", "Merlin", "Robin")
        default_specialization = ("WARRIOR", "MAGE", "ROGUE")
        for i in range(0, 3):
            party_members.append(
                PlayableActor(
                    default_names[i],
                    default_specialization[i],
                )
            )

        return PlayerParty(
            members=party_members,
            name="The Default Party",
        )

    @staticmethod
    def get_start_type() -> str:
        if os.path.exists("use_default.flag") is True:
            return "USE_DEFAULT"
        match os.path.exists("savegame.rpygs"):
            case True:
                start_game_options = ["NEW", "LOAD"]
                start_game_messages = [
                    "Would you like to Start a new game or Load an existing save?",
                    "Options are:",
                ]
            case False:
                start_game_options = ["NEW"]
                start_game_messages = [
                    "Type 'NEW' to start a new game",
                    "You will be able to save your game later and load it here",
                    "Options are:",
                ]
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise ImpossibleValueException(  # pyright: ignore[reportUnreachable]
                    "os.path.exists('savegame.rpygs') did not return a bool and something is very wrong"
                )

        core_io = CoreIO.get_core_io()
        core_io.send_output(
            OutputMessage("Welcome to RPyG, a text based RPG in Python")
        )
        core_io.request_input(
            UserPromptRequest(
                options=start_game_options,
                prompts=start_game_messages,
            )
        )
        player_action = core_io.receive_input()
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

        core_io.request_input(
            UserPromptRequest(
                options=party_size_choices,
                prompts=party_size_messages,
            )
        )
        party_size = int(core_io.receive_input())

        party_instances: list[PlayableActor] = []
        for _ in range(0, party_size):
            core_io = CoreIO.get_core_io()
            core_io.request_input(
                CustomTextRequest(
                    prompts=member_name_messages,
                    max_length=32,
                )
            )
            member_name = core_io.receive_input()
            core_io.request_input(
                UserPromptRequest(
                    prompts=specialization_messages,
                    options=specialization_choices,
                )
            )
            member_specialization = core_io.receive_input()
            member = PlayableActor(member_name, member_specialization)
            party_instances.append(member)

        core_io.request_input(
            CustomTextRequest(
                prompts=party_name_messages,
                max_length=64,
            )
        )
        party_name = core_io.receive_input()

        return GameState(PlayerParty(party_name, party_instances))

    @staticmethod
    def load_game() -> GameState:
        """
        Call this to load the game stored in the pickle file called 'savegame.rpygs'.
        Any other .rpygs files will be ignored
        """
        save_file_path = "savegame.rpygs"
        core_io = CoreIO.get_core_io()

        # Check if the save file exists
        if not os.path.exists(save_file_path):
            raise FileNotFoundError(
                "Save file not found. Please check file path & try again, or start a new game"
            )

        with open(save_file_path, "rb") as save_file:
            content = save_file.read()
        signature, serialized_data = content[:32], content[32:]  # Assuming SHA-256 hash
        expected_signature = hmac.new(
            secret_key, serialized_data, hashlib.sha256
        ).digest()

        match hmac.compare_digest(expected_signature, signature):
            case True:
                game_state: GameState = pickle.loads(serialized_data)
            case False:
                raise ValueError("Save file tampered with or corrupted.")
            case _:  # pyright: ignore[reportUnnecessaryComparison]
                raise RuntimeError(  # pyright: ignore[reportUnreachable]
                    "Save File tampering is so bad that compare_digest did not return a bool MonkaS"
                )

        ensure_type(game_state, GameState, "game_state")

        core_io.send_output(
            OutputMessage(
                f"Successfully Loaded Save Game for: {game_state.player_party.name}"
            )
        )
        ## yuck but I am moving off of pickle soon anyways
        GameState._instance = game_state  # pyright: ignore[reportPrivateUsage]
        return game_state
