import os

from RPyG.actors import PlayerParty
from RPyG.actors.actor_playable import PlayableActor
from RPyG.core_io import CoreIO
from RPyG.gameState.file import load_game


def get_start_type() -> str:
    if os.path.exists("savegame.rpygs") is True:
        start_game_options = ["NEW", "LOAD"]
        start_game_messages = [
            "Would you like to Start a new game or Load an existing save?",
            "NOTE: All Prompts in this game are case insensitive",
            "Options are:",
        ]

    else:
        start_game_options = ["NEW"]
        start_game_messages = [
            "Type 'NEW' to start a new game",
            "You will be able to save your game later and load it here",
            "NOTE: All Prompts in this game are case insensitive",
            "Options are:",
        ]
    core_io = CoreIO.get_core_io()
    core_io.request_input(
        {
            "options": start_game_options,
            "messages": start_game_messages,
        }
    )
    player_action = core_io.receive_input()
    return player_action


def party_start() -> tuple[list[list[str]], str]:
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

    core_io.request_input()
    party_size = int(
        core_io.receive_input(
            {
                "choices": party_size_choices,
                "messages": party_size_messages,
                "return_index": True,
            }
        )
    )

    party_member_attribs: list[list[str]] = []
    for _ in range(0, party_size):
        core_io = CoreIO.get_core_io()
        core_io.request_input(
            {
                "type": "custom_text_entry",
                "messages": member_name_messages,
                "max_len": 32,
            }
        )
        member_name = core_io.receive_input()
        core_io.request_input(
            {
                "choices": specialization_choices,
                "message": specialization_messages,
            }
        )
        member_specialization = core_io.receive_input()
        member_attrib = [member_name, member_specialization]
        party_member_attribs.append(member_attrib)
    core_io.request_input(
        {
            "type": "custom_text_entry",
            "messages": party_name_messages,
            "max_len": 32,
        }
    )
    party_name = core_io.receive_input()

    return party_member_attribs, party_name


def default_party() -> list[PlayableActor]:
    party_members: list[PlayableActor] = []
    default_names = ("Conan", "Merlin", "Robin")
    default_specialization = ("WARRIOR", "MAGE", "ROGUE")
    for i in range(0, 3):
        member = (default_names[i], default_specialization[i])
        party_members.append(PlayableActor(member[0], member[1]))
    return party_members


def start_game() -> PlayerParty:
    core_io = CoreIO.get_core_io()
    core_io.send_output("Welcome to RPyG, a text based RPG in Python")

    welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----
"""
    core_io.send_output(welcome_message)

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
