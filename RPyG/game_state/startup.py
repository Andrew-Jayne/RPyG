import os

from RPyG.actors import PlayableActor, PlayerParty
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import CustomTextRequest, OutputMessage, UserPromptRequest
from RPyG.exceptions import ImpossibleValueException


def default_party() -> PlayerParty:
    party_members: list[PlayableActor] = []
    default_names = ("Conan", "Merlin", "Robin")
    default_specialization = ("WARRIOR", "MAGE", "ROGUE")
    for i in range(0, 3):
        member = (default_names[i], default_specialization[i])
        party_members.append(PlayableActor(member[0], member[1]))

    return PlayerParty(
        members=party_members,
        name="The Default Party",
    )


def get_start_type() -> str:
    core_io = CoreIO.get_core_io()
    core_io.send_output(OutputMessage("Welcome to RPyG, a text based RPG in Python"))
    if os.path.exists("use_default.flag"):
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

    core_io.request_input(
        UserPromptRequest(
            options=start_game_options,
            prompts=start_game_messages,
        )
    )
    player_action = core_io.receive_input()
    return player_action


def party_start() -> tuple[list[tuple[str, str]], str]:
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

    party_member_attribs: list[tuple[str, str]] = []
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
        member_attrib: tuple[str, str] = (member_name, member_specialization)
        party_member_attribs.append(member_attrib)

    core_io.request_input(
        CustomTextRequest(
            prompts=party_name_messages,
            max_length=64,
        )
    )
    party_name = core_io.receive_input()

    return (party_member_attribs, party_name)
