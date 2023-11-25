import time
from interaction.interaction import Interaction

def flee_success_message(enemy_name):
    print(f"You Successfuly Escape the {enemy_name}!")

def flee_failure_message(enemy_name):
    print(f"You Fail to Escape the {enemy_name}!")
    if Interaction.global_game_mode != "AUTO":
        time.sleep(2)