from interaction.interaction import Interaction
from display.display import Display

def get_start_type():

    type_message = """
Would you like to Start a new game or Load an existing save?
Options are : NEW & LOAD


Note: All Prompts in this game are case insensitive

"""
    type_choices = ["NEW", "LOAD"]
    player_action = Interaction.validate_input(type_choices, type_message)
    Display.clear_display()
    return player_action

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

    
def player_start():

    player_name_message = """
Now before your journey can begin please enter the name of your Character


Note: Case is respected but names longer than 32 characters will be truncated

"""
    player_name = Interaction.sanitize(str(input(f"{player_name_message}"))[:32])
    Display.clear_display()
    return player_name


























### moved this way down here because I don't even want to loook at it lmao
def multiplayer_start(): ## Unused for now, pending other changes to the gameplay
    players = []
    count_choices = ["1","2","3","4"]
    count_message = """
Choose the number of players:
1
2
3
4

    """
    player_count = int(Interaction.validate_input(count_choices, count_message))
    Interaction.global_player_count = player_count

    player_name_message = """
Now before your Journey Can Begin Please enter the name of your Character


Note: Case is respected but names longer than 32 Characters will be truncated

"""

    if Interaction.global_game_mode == "MANUAL":
        for count in range(0,Interaction.global_player_count):
            player_name = str(input(f"{player_name_message}"))[:32]
            players.append(player_name)
    else:
         for count in range(0,Interaction.global_player_count):
            players.append(f"The Protagonist{count}")

    return players