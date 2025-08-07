import os

from RPyG.actors import PlayerParty
from RPyG.actors.actor_playable import PlayableActor
from RPyG.core_io import CoreIO
from RPyG.core_io.io_models import CustomTextRequest, OutputMessage, UserPromptRequest
from RPyG.gameState.file import load_game


def get_start_type() -> str:
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
        case _:
            raise RuntimeError(
                "os.path.exists('savegame.rpygs') did not return a bool and something is very wrong"
            )

    core_io = CoreIO.get_core_io()
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

    party_member_attribs: list[list[str]] = []
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


def start_game() -> PlayerParty:
    core_io = CoreIO.get_core_io()
    core_io.send_output(OutputMessage("Welcome to RPyG, a text based RPG in Python"))
    match get_start_type():
        case "LOAD":
            return load_game()
        case "NEW":
            my_party, my_party_name = party_start()
            my_party_instances: list[PlayableActor] = []
            for member in my_party:
                my_party_instances.append(PlayableActor(member[0], member[1]))
            return PlayerParty(my_party_name, my_party_instances)
        case _:
            raise ValueError("Invalid Game Start Type")
