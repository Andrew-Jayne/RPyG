from interaction.interaction import Interaction
from display.display import Display
from actors.actor_player import Player

def welcome():
    print("Welcome to RPyG, a text based RPG in Python", end="\n\n")

    mode_message = """
             This game looks best with a width of at least 80.
            If the next line is split please widen your terminal.
----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----


Please Select your Game mode:
Options are : Manual & Auto

Note: All Prompts in this game are case insensitive

"""
    mode_choices = ["AUTO", "MANUAL"]
    Interaction.global_game_mode = Interaction.validate_input(mode_choices, mode_message)
    Display.clear_display()

def get_start_type():

    type_message = """
Would you like to Start a new game or Load an existing save?
Options are : NEW & LOAD

"""
    type_choices = ["NEW", "LOAD"]
    player_action = Interaction.validate_input(type_choices, type_message)
    Display.clear_display()
    return player_action

class PartyMember():
    def __init__(self, name:str, specialization:str):
        self.name = name
        self.specialization = specialization
        

def party_start():
    party_size_choices = ["1","2","3"]
    specialization_choices = ["WARRIOR", "MAGE", "ROGUE"]
    party_size_message = """
How many members are in your party?
1
2
3

"""
    specialization_messages = """
What Specalization will this member use?
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

    party_size = int(Interaction.validate_input(party_size_choices, party_size_message)) #kinda Yikes but casting str to int is not horendously unsafe
    party_members = []
    for _ in range(0,party_size):
        member_name =  Interaction.custom_text_entry(member_name_message, 32)
        member_specialization = Interaction.validate_input(specialization_choices,specialization_messages)
        member = PartyMember(member_name, member_specialization)
        party_members.append(member)
    party_name = Interaction.custom_text_entry(party_name_message, 64)
    return party_members, party_name




def default_party():
    party_members = []
    default_names = ["Conan","Merlin","Robin"]
    default_specialization = ["WARRIOR", "MAGE", "ROGUE"]
    for i in range(0,3):
        member = PartyMember(default_names[i], default_specialization[i])
        player_member = Player(name=member.name, specialization=member.specialization)
        party_members.append(player_member)
    return party_members
