from interaction import Interaction

def welcome():
    game_mode = None
    print("Welcome to RPyG, a text based RPG in Python", end="\n\n")

    mode_choices = ["AUTO", "MANUAL"]

    mode_message = """
Please Select your Game mode:
Options are : Manual & Auto


Note: All Prompts in this game are case insensitive

"""

    game_mode = Interaction.validate_input(mode_choices, mode_message)
    Interaction.global_game_mode = game_mode

    player_name_message = """
Now before your Journey Can Begin Please enter the name of your Character


Note: Case is respected but names longer than 32 Characters will be truncated

"""              

    if Interaction.global_game_mode == "MANUAL":
        player_name = str(input(f"{player_name_message}"))[:32]
    else:
        player_name = "The Protagonist"

    return player_name