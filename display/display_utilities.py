import os
from interaction.interaction import Interaction

def clear_display():
    ## Screen is not cleared in Auto mode since It's better for testing and Auto mode is kinda turning into a debug mode (I might make that an option at some point)
    if Interaction.global_game_mode != "AUTO":
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For macOS and Linux
        else:
            os.system('clear')