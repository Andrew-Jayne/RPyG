## Player Messages
import time
from interaction.interaction import Interaction
from display.display_utilities import clear_display

def player_progress_message(player_instance):
    print(f"""
You Progress 10 Miles further.
You have traveled {player_instance.progress * 10} Miles Total.
""")
    ## Don't pause for effect when in full auto mode
    if Interaction.global_game_mode != "AUTO":
        time.sleep(2)
    ## Clear the Display after 10 Steps
    if player_instance.progress % 10 == 0:
        clear_display()
    

def player_attack_message(player_instance):
    print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power} damage", end="\n\n")


def player_critical_attack_message(player_instance):
    print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power * 2} damage")
    print(f"{player_instance.name} got a critical hit!!", end="\n\n")