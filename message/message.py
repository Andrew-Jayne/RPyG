import time
import pickle
from actors.actor_player import Player
from interaction.interaction import Interaction
from actors.actor_follower import Follower
from display.display import Display

class Message():
    # Actor Messages
    @staticmethod
    def defeated_message(actor_name):
        print(f"{actor_name} has been defeated" , end='\n\n')
    
    @staticmethod
    def encounter_message(actor_name):
        print(f"You encounter a {actor_name}!", end="\n\n")
    
    @staticmethod
    def actor_health_message(actor_instance):
        print(f"{actor_instance.name} has {actor_instance.health} Health remaining", end="\n\n")
    
    @staticmethod
    def actor_attack_message(attacker_instance):
        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, Follower) != True and isinstance(attacker_instance, Player) != True:
            time.sleep(2)
        if isinstance(attacker_instance, Player) == True:
            attacker_name_action = "You attack"
        else:
            attacker_name_action = f"{attacker_instance.name} attacks"
        print(f"{attacker_name_action} with {attacker_instance.attack_name} inflicting {attacker_instance.attack_power} damage", end="\n\n")

    @staticmethod
    def actor_critical_attack_message(attacker_instance):
        # Only Pause when the game is in manual and the generic actor is not a follower
        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, Follower) != True and isinstance(attacker_instance, Player) != True:
            time.sleep(2)
        if isinstance(attacker_instance, Player) == True:
            attacker_name_action = "You attack"
        else:
            attacker_name_action = f"{attacker_instance.name} attacks"
        print(f"{attacker_name_action} with {attacker_instance.attack_name} inflicting {attacker_instance.attack_power * 2} damage")
        print(f"{attacker_instance.name} got a critical hit!!", end="\n\n")




    # Battle Messages
    @staticmethod
    def battle_hud_message(playable_instance, enemy_instance):
        print(f"{playable_instance.name}: {playable_instance.health}")
        print(f"{enemy_instance.name}: {enemy_instance.health}")
    
    @staticmethod
    def battle_start_message():
        print("The Battle Begins!", end="\n\n\n")



    # Encouter Messages
    @staticmethod
    def flee_failure_message(enemy_name):
        print(f"You Fail to Escape the {enemy_name}!")
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
    
    @staticmethod
    def flee_success_message(enemy_name):
        print(f"You Successfuly Escape the {enemy_name}!")

    @staticmethod
    def evade_prep_message():
        print("You prepare to evade the next attack", end="\n\n")

    @staticmethod
    def evade_failure_message():
        print("You fail to evade the attack!", end="\n\n")

    @staticmethod
    def evade_sucess_message():
        print("You deftly evade the enemy's attack!")


    # Player Messages
    
    @staticmethod
    def player_progress_message(player_instance):
        print(f"""
You Progress 10 Miles further.
You have traveled {player_instance.progress * 10} Miles Total.
""")
        ## Pause for effect when in MANUAL mode
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
        ## Clear the Display after 10 Steps
        if player_instance.progress % 10 == 0:
            Display.clear_display()

    @staticmethod
    def post_game_recap(player_instance):
        # Post Game Report
        print(f"Player Name: {player_instance.name}")
        print(f"Player Base Health: {player_instance.base_health}")
        print(f"Player Int: {player_instance.intellect}")
        print(f"Player Str: {player_instance.strength}")
        print(f"Player Agl: {player_instance.agility}")
        print(f"Player Lck: {player_instance.luck}")
        print(f"Player Gold: {player_instance.gold}")
        print(f"Player Potions: {player_instance.potions}")
        print(f"Player Attack: {player_instance.attack_name}")
        print(f"Player Skill: {player_instance._get_skill()}")

        print(f"Player Has Follower?: {player_instance.has_follower}")
        if player_instance.has_follower == True:
            print(f"Player Follower is {player_instance.follower_instance.__dict__}")

    @staticmethod
    def end_game_message(player_instance):
        print(f"Fortranus the Ancient One has been Vanquished at the hands of {player_instance.name}")
        print("Your adventure has been completed, you may start a new adventure if you so choose")
        if Interaction.global_game_mode == "MANUAL":
            with open('savegame.rpygs', 'wb') as save_file:
                # Write some text to the file.
                pickle.dump(player_instance, save_file)
                exit()
                # The file is automatically closed when you exit the 'with' block.