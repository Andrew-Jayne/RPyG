import time
from file.file import save_game
from actors.actor_playable import PlayableActor
from interaction.interaction import Interaction
from display.display import Display

class Message():
    # Actor Messages
    @staticmethod
    def defeated_message(name:str) -> None:
        print(f"{name} has been defeated" , end='\n\n')
    
    @staticmethod
    def encounter_message(group_name:str) -> None:
        print(f"Your Party encounters a {group_name}!", end="\n\n")
    
    @staticmethod
    def actor_health_message(actor_instance:object) -> None:
        print(f"{actor_instance.name} has {actor_instance.health} Health remaining", end="\n\n")
    
    @staticmethod
    def actor_attack_message(attacker_instance:object, damage_value:int) -> None:
        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, PlayableActor) == False:
            time.sleep(2)
        print(f"{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value} damage", end="\n\n")

    @staticmethod
    def actor_critical_attack_message(attacker_instance:object, damage_value:int) -> None:
        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, PlayableActor) == False:
            time.sleep(2)
        print(f"{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value * 2} damage")
        print(f"{attacker_instance.name} got a critical hit!!", end="\n\n")

    def poison_damage_message(actor_instance:object) -> None:
        print(f"{actor_instance.name} takes {actor_instance.poison_damage} from being poisoned")

    # Battle Messages
    @staticmethod
    def battle_hud_message(player_party_instance:object, enemy_party_instance:object) -> None:
        for playable_instance in player_party_instance.members:
            print(f"{playable_instance.name}: {playable_instance.health}")
        for enemy_instance in enemy_party_instance.members:
            print(f"{enemy_instance.name}: {enemy_instance.health}")
        print("\n\n")
    
    @staticmethod
    def battle_start_message() -> None:
        print("The Battle Begins!", end="\n\n\n")

    # Encounter Messages
    @staticmethod
    def flee_failure_message(player_name:str, enemy_name:str) -> None:
        print(f"{player_name} has Failed to Escape the {enemy_name}!")
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
    
    @staticmethod
    def flee_success_message(player_name:str, enemy_name:str) -> None:
        print(f"{player_name} has Successfuly Escaped the {enemy_name}!")

    @staticmethod
    def evade_prep_message(name:str) -> None:
        print(f"{name} prepares to evade the next attack", end="\n\n")

    @staticmethod
    def evade_failure_message(name:str) -> None:
        print(f"{name} fails to evade the attack!", end="\n\n")

    @staticmethod
    def evade_success_message(name:str) -> None:
        print(f"{name} deftly evades the enemy's attack!")


    # Player Messages
    
    @staticmethod
    def party_progress_message(party_instance:object) -> None:
        print(f"""
Your Party Progresses 10 Miles further.
They have traveled {party_instance.progress * 10} Miles Total.
""")
        ## Pause for effect when in MANUAL mode
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
        ## Clear the Display after 10 Steps
        if party_instance.progress % 10 == 0:
            Display.clear_display()

    @staticmethod
    def post_game_recap(player_party_instance:object) -> None:
        for player_instance in player_party_instance.members:
        # Post Game Report
            print(f"Player Name: {player_instance.name}")
            print(f"Player Base Health: {player_instance.base_health}")
            print(f"Player Final Health: {player_instance.health}")
            print(f"Player Int: {player_instance.intellect}")
            print(f"Player Str: {player_instance.strength}")
            print(f"Player Agl: {player_instance.agility}")
            print(f"Player Lck: {player_instance.luck}")
            print(f"Player Gold: {player_instance.gold}")
            print(f"Player Potions: {player_instance.potions}")
            print(f"Player Attack: {player_instance.attack_name}")
            print("")

    @staticmethod
    def end_game_message(player_party_instance:object) -> None:
        print(f"Fortranus the Ancient One has been Vanquished at the hands of {player_party_instance.name}")
        print("Your adventure has been completed, you may start a new adventure if you so choose")
        if Interaction.global_game_mode == "MANUAL":
            save_game(player_party_instance)