import time
import textwrap
import json
from gameState.file import save_game
from actors.actor_playable import PlayableActor
from interaction.interaction import Interaction
from display.display import Display


# Only used for Type checking/Hinting
from actors.actor_party import PlayerParty, EnemyParty
from actors.actor_combatant import Combatant


class Message():
    @staticmethod
    def display_message(message:str,new_line_count:int) -> None:
        """
Use this function rather than local 'print() in functions/
This does basic processing for optimal display and will allow for better output handling when the UI is redone
        """
        ending = ("\n" * new_line_count)

        print(textwrap.fill(message, width=80),end=ending)

    # Actor Messages
    @staticmethod
    def defeated_message(name:str) -> None:
        print(f"{name} has been defeated" , end='\n\n')
    
    @staticmethod
    def encounter_message(group_name:str) -> None:
        print(f"Your Party encounters a {group_name}!", end="\n\n")
    
    @staticmethod
    def actor_health_message(actor_instance:Combatant) -> None:
        if not isinstance(actor_instance, Combatant):
            raise ValueError("The 'actor_instance' parameter must be of type Combatant. Received type: {}".format(type(actor_instance).__name__))
        
        print(f"{actor_instance.name} has {actor_instance.health} Health remaining", end="\n\n")
    
    @staticmethod
    def actor_attack_message(attacker_instance:Combatant, damage_value:int) -> None:
        if not isinstance(attacker_instance, Combatant):
            raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))

        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, PlayableActor) == False:
            time.sleep(2)
        print(f"{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value} damage", end="\n\n")

    @staticmethod
    def actor_critical_attack_message(attacker_instance:Combatant, damage_value:int) -> None:
        if not isinstance(attacker_instance, Combatant):
            raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))

        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, PlayableActor) == False:
            time.sleep(2)
        print(f"{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value * 2} damage")
        print(f"{attacker_instance.name} got a critical hit!!", end="\n\n")


    # Battle Messages
    @staticmethod
    def battle_hud_message(player_party_instance:PlayerParty, enemy_party_instance:EnemyParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        if not isinstance(enemy_party_instance, EnemyParty):
            raise ValueError("The 'enemy_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(enemy_party_instance).__name__))


        for playable_instance in player_party_instance.members:
            print(f"{playable_instance.name}: {playable_instance.health}")
        print("")
        for enemy_instance in enemy_party_instance.members:
            print(f"{enemy_instance.name}: {enemy_instance.health}")
        print("\n\n")
    
    @staticmethod
    def battle_start_message() -> None:
        print("The Battle Begins!", end="\n\n\n")

    # Encounter Messages
    @staticmethod
    def distance_since_last(no_encounters_since:int) -> None:
        print(f"After {no_encounters_since * 10} miles of travel")   

    @staticmethod
    def flee_failure_message(player_name:str, enemy_name:str) -> None:
        print(f"{player_name} has Failed to Escape the {enemy_name}!")
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
    
    @staticmethod
    def flee_success_message(player_name:str, enemy_name:str) -> None:
        print(f"{player_name} has Successfully Escaped the {enemy_name}!")

    def special_encounter_message(progress_value:int, party_name:str,message_type:str)-> None:
        if message_type not in ["messages","success_messages","failure_messages"]:
            raise ValueError('Message type must be one of ["messages","success_messages","failure_messages"]')
        with open('encounters/story_events.json') as file:
            story_events_list = json.load(file)


        all_events = story_events_list['progress_events']

        current_event = all_events[str(progress_value)]
        for message in current_event[message_type]:
            formatted_message = message.format(party_name=party_name)

            print(textwrap.fill(formatted_message, width=80), end="\n\n")
            if Interaction.global_game_mode == "MANUAL":
                time.sleep(2)


    # Player Messages
    
    @staticmethod
    def party_progress_message(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        print(f"""
Your Party Progresses 10 Miles further.
They have traveled {player_party_instance.progress * 10} Miles Total.
""")
        ## Pause for effect when in MANUAL mode
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
        ## Clear the Display after 10 Steps
        if player_party_instance.progress % 10 == 0:
            Display.clear_display()

    @staticmethod
    def post_game_recap(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))


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
            print(f"Player Attack Name: {player_instance.attack_name}")
            print(f"Player Attack Power: {player_instance.attack_power}")
            print("")

    @staticmethod
    def end_game_message(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        print(f"Fortranus the Ancient One has been Vanquished at the hands of {player_party_instance.name}",end="\n\n")
        print("Your adventure has been completed, you may start a new adventure if you so choose",end="\n\n")
        if Interaction.global_game_mode == "MANUAL":
            save_game(player_party_instance)

    @staticmethod
    def empty_travel_message(empty_distance:int) -> None:
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
        print(f"{'.' * (empty_distance - 1 )}")