import os
from typing import overload

from RPyG.constructs import PlayableActor, PlayerParty
from RPyG.core_io import CoreIO, input_models, output_models
from RPyG.exceptions import ImpossibleValueException
from RPyG.game_state import GameState
from RPyG.utilities import ensure_type


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
    limited_string = input_string[:max_length]  # Limit the input to the desired length
    for literal in literal_control_strings:
        limited_string = limited_string.replace(literal, "")
    cleaned_string = ""
    for char in limited_string:
        if char not in chars_to_remove and char not in control_chars:
            cleaned_string += char

    return cleaned_string


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


def clear_display() -> None:
    # For Windows
    if os.name == "nt":
        os.system("cls")  # pyright: ignore[reportUnusedCallResult]
    # For macOS and Linux
    else:
        os.system('clear && printf "\\e[3J"')  # pyright: ignore[reportUnusedCallResult]


def validate_input(choice_list: list[int]) -> int:
    """
    Checks that the string input by the user is in the allowed list of responses
    Sanitizes the input then returns up to the max length specified
    """

    def invalid_choice(dumb_check: int):
        core_io.send_output(
            output_models.OutputMessage(
                message=f"That is not a Valid Option. Try again, valid options are \n{str(choice_list)}"
            )
        )

        if dumb_check == 10:
            raise ValueError("Look it's not hard, just enter a valid choice....")

    core_io = CoreIO.get_core_io()
    chosen_action = -1
    dumb_check = 0
    while chosen_action not in choice_list:
        dumb_check += 1
        try:
            chosen_action = int(sanitize(input().upper()))
        except ValueError:
            invalid_choice(dumb_check)
            continue
        if chosen_action not in choice_list:
            invalid_choice(dumb_check)

    return chosen_action


def custom_text_entry(
    input_messages: list[str],
    max_length: int,
) -> str:
    core_io = CoreIO.get_core_io()
    core_io.send_output(output_models.OutputMessage(message="\n".join(input_messages)))
    return sanitize(input()[:max_length])


def prompt_user(
    options: list[str],
    prompts: list[str],
    show_prompts: bool = True,
    return_index: bool = False,
) -> str | int:
    """
    Takes in a list of options, and list of prompts
    Shows Prompts by default
    returns the option at the selected index
    """
    ensure_type(options, list, "options")
    ensure_type(prompts, list, "prompts")

    formatted_message = ""
    if show_prompts is True:
        for message in prompts:
            formatted_message += f"{message}\n"
    formatted_message += "\n"
    index = 0
    for option in options:
        formatted_message += f"[{index}] {option}\n"
        index += 1

    formatted_message += "\n"
    core_io = CoreIO.get_core_io()
    core_io.send_output(output_models.OutputMessage(message=formatted_message))

    if return_index is True:
        return validate_input(list(range(0, index)))

    return options[validate_input(list(range(0, index)))]


def get_start_type() -> str:
    if os.path.exists(os.path.expanduser("~/.rpyg/savegame.rpygs")) is True:
        start_game_options = ["NEW", "LOAD", "USE_DEFAULT"]
        start_game_messages = [
            "Would you like to Start a new game or Load an existing save?",
            "Options are:",
        ]
    else:
        start_game_options = ["NEW", "USE_DEFAULT"]
        start_game_messages = [
            "Type 'NEW' to start a new game",
            "You will be able to save your game later and load it here",
            "Select 'USE_DEFAULT' to start a new game with the default party",
            "Options are:",
        ]

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
