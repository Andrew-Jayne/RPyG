import os
from interaction.interaction import Interaction
from message.message import Message
from display.display import Display
from actors.actor_playable import PlayableActor


def welcome() -> None:
    Message.display_message("Welcome to RPyG, a text based RPG in Python", 2)

    welcome_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----
"""
    Message.display_message(welcome_message, 1)

def get_start_type() -> str:

    if os.path.exists('savegame.rpygs'):
        new_and_load_message = """
Would you like to Start a new game or Load an existing save?
Options are : NEW & LOAD


NOTE: All Prompts in this game are case insensitive

"""  
        new_and_load_choices = ["NEW", "LOAD"]
        player_action = Interaction.validate_input(new_and_load_choices, new_and_load_message)      

    else:
        new_game_message = """
Type "NEW" to start a new game
You will be able to save your game later and load it here

Options are : NEW


NOTE: All Prompts in this game are case insensitive
"""
        new_game_choices = ["NEW", "LOAD"]
        player_action = Interaction.validate_input(new_game_choices, new_game_message)
        Display.clear_display()
    return player_action


def party_start() -> tuple:
    party_size_choices = ["1","2","3"]
    specialization_choices = ["WARRIOR", "MAGE", "ROGUE"]
    party_size_message = """
How many members are in your party?
1
2
3

"""
    specialization_messages = """
What Specialization will this member use?
WARRIOR
MAGE
ROGUE

"""

    member_name_message = """
Before their journey can begin you must name your Character

Note: Case is respected but names longer than 32 characters will be truncated

"""

    party_name_message = """
Before their journey can begin you must name your Party

Note: Case is respected but names longer than 64 characters will be truncated

"""

    party_size = int(Interaction.validate_input(party_size_choices, party_size_message)) #kinda Yikes but casting str to int is not horrendously unsafe
    party_members = []
    for _ in range(0,party_size):
        member_name =  Interaction.custom_text_entry(member_name_message, 32)
        member_specialization = Interaction.validate_input(specialization_choices,specialization_messages)
        member = [member_name, member_specialization]
        party_members.append(member)
    party_name = Interaction.custom_text_entry(party_name_message, 64)
    Display.clear_display()
    return party_members, party_name


def default_party() -> list:
    party_members = []
    default_names = ("Conan","Merlin","Robin")
    default_specialization = ("WARRIOR", "MAGE", "ROGUE")
    for i in range(0,3):
        member = (default_names[i], default_specialization[i])
        party_members.append(PlayableActor(member[0], member[1]))
    return party_members
