from interaction import Interaction

def welcome():
    game_mode = None
    print("Welcome to RPyG, a text based RPG in Python", end="\n\n")

    mode_message = """
Please Select your Game mode:
Options are : Manual & Auto


Note: All Prompts in this game are case insensitive

"""

    player_name_message = """
Now before your Journey Can Begin Please enter the name of your Character


Note: Case is respected but names longer than 32 Characters will be truncated

"""
    
    dumb_check = 0 
    while game_mode == None:
        mode = str(input(f"{mode_message}")).lower()
        match mode:
            case "manual":
                game_mode = "MAN"
            case "auto":
                game_mode = "AUTO"
            case _:
                print("error invalid choice, try again")
                dumb_check += 1
                if dumb_check == 10:
                    print("Look it's not hard, just enter a valid choice....", end="\n\n")
                    exit()
    Interaction.global_game_mode = game_mode

    if Interaction.global_game_mode == "MAN":
        player_name = str(input(f"{player_name_message}"))[:32]
    else:
        player_name = "The Protagonist"


    return player_name
