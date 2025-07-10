import os

from actors import PlayerParty
from actors.actor_playable import PlayableActor
from config import update_global_game_mode
from display.display import Display
from gameState.file import load_game
from interaction.interaction import Interaction
from message.message import Message


def welcome() -> None:
    Message.display_message("Welcome to RPyG, a text based RPG in Python", 2)

    welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----
"""
    Message.display_message(welcome_message, 3)


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

    player_action = Interaction.prompt_user(start_game_options, start_game_messages)
    Display.clear_display()
    return player_action


def party_start() -> tuple:
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

    party_size = Interaction.prompt_user(
        party_size_choices, party_size_messages, return_int=True
    )
    Display.clear_display()

    party_members = []
    for _ in range(0, party_size):
        member_name = Interaction.custom_text_entry(member_name_messages, 32)
        member_specialization = Interaction.prompt_user(
            specialization_choices, specialization_messages
        )
        member_attrib = [member_name, member_specialization]
        party_members.append(member_attrib)
        Display.clear_display()

    party_name = Interaction.custom_text_entry(party_name_messages, 64)
    Display.clear_display()

    return party_members, party_name


def default_party() -> list:
    party_members = []
    default_names = ("Conan", "Merlin", "Robin")
    default_specialization = ("WARRIOR", "MAGE", "ROGUE")
    for i in range(0, 3):
        member = (default_names[i], default_specialization[i])
        party_members.append(PlayableActor(member[0], member[1]))
    return party_members


def start_game(game_mode: str, using_default_party: bool) -> PlayerParty:
    welcome()
    match game_mode:
        case "AUTO":
            update_global_game_mode("AUTO")
            return PlayerParty(name="The Default Party", members=default_party())
        case "MANUAL":
            update_global_game_mode("MANUAL")
            if using_default_party is True:
                return PlayerParty(name="The Default Party", members=default_party())
            else:
                match get_start_type():
                    case "LOAD":
                        return load_game()
                    case "NEW":
                        my_party, my_party_name = party_start()
                        my_party_instances = []
                        for member in my_party:
                            my_party_instances.append(
                                PlayableActor(member[0], member[1])
                            )
                        return PlayerParty(my_party_name, my_party_instances)
        case _:
            raise ValueError("Error No Valid Game Mode was selected")
