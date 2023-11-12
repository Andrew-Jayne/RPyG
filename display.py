import os
import time
from interaction import Interaction


class Display:

    @staticmethod
    def clear_display():
        ## Screen is not cleared in Auto mode since It's better for testing and Auto mode is kinda turning into a debug mode (I might make that an option at some point)
        if Interaction.global_game_mode != "AUTO":
            # For Windows
            if os.name == 'nt':
                os.system('cls')
            # For macOS and Linux
            else:
                os.system('clear')

## Player Messages
    @staticmethod
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
            __class__.clear_display()
        
    @staticmethod
    def player_attack_message(player_instance):
        print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power} damage", end="\n\n")



    @staticmethod
    def player_critical_attack_message(player_instance):
        print(f"You Attack with {player_instance.attack_name} and inflict {player_instance.attack_power * 2} damage")
        print(f"{player_instance.name} got a critical hit!!", end="\n\n")


## Generic Actor Messages

    @staticmethod
    def encounter_message(actor_name):
        print(f"You encounter a {actor_name}!", end="\n\n")

    @staticmethod
    def defeated_message(actor_instance):
        print(f"{actor_instance.name} has been defeated" , end='\n\n')

    @staticmethod
    def actor_attack_message(actor_instance):
        if Interaction.global_game_mode != "AUTO":
            time.sleep(2)
        print(f"{actor_instance.name} attacks with {actor_instance.attack_name} inflicting {actor_instance.attack_power} damage", end="\n\n")

    @staticmethod
    def actor_critical_attack_message(actor_instance):
        if Interaction.global_game_mode != "AUTO":
            time.sleep(2)
        print(f"{actor_instance.name} attacks with {actor_instance.attack_name} inflicting {actor_instance.attack_power * 2} damage")
        print(f"{actor_instance.name} got a critical hit!!", end="\n\n")


    @staticmethod
    def actor_health_message(actor_instance):
        print(f"{actor_instance.name} has {actor_instance.health} Health remaining", end="\n\n")



## Battle Special Messages:
    @staticmethod
    def battle_hud_message(player_instance, enemy_instance):
        print(f"{player_instance.name}: {player_instance.health}")
        if player_instance.has_follower == True:
            print(f"{player_instance.follower_instance.name}: {player_instance.follower_instance.health}")
        print(f"{enemy_instance.name}: {enemy_instance.health}")
    
    @staticmethod
    def battle_start_message():
        print("The Battle Begins!", end="\n\n\n")


##  Encounter Messages

    @staticmethod
    def flee_success_message(enemy_name):
        print(f"You Successfuly Escape the {enemy_name}!")

    @staticmethod
    def flee_failure_message(enemy_name):
        print(f"You Fail to Escape the {enemy_name}!")
        if Interaction.global_game_mode != "AUTO":
            time.sleep(2)