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
    def display_message(message: str, new_line_count: int) -> None:
        """
        Use this function rather than local 'print()' in functions.
        This does basic processing for optimal display and will allow for better output handling when the UI is redone.
        """
        ending = "\n" * new_line_count
        wrapped_message = ""

        # Split the message into lines to handle them individually
        lines = message.split('\n')
        for line in lines:
            # Apply text wrapping to each line individually
            wrapped_line = textwrap.fill(line, width=80)
            wrapped_message += wrapped_line + "\n"

        # Print the final wrapped message, removing the last added newline and adding the custom ending
        print(wrapped_message.rstrip('\n'), end=ending)

    # Actor Messages
    @staticmethod
    def defeated_message(name:str) -> None:
        defeated_message = f"{name} has been defeated"

        __class__.display_message(defeated_message, 2)
    
    @staticmethod
    def encounter_message(group_name:str) -> None:
        encounter_message = f"Your Party encounters a {group_name}!"

        __class__.display_message(encounter_message, 2)
    
    @staticmethod
    def actor_health_message(actor_instance:Combatant) -> None:
        if not isinstance(actor_instance, Combatant):
            raise ValueError("The 'actor_instance' parameter must be of type Combatant. Received type: {}".format(type(actor_instance).__name__))
        
        actor_health_message = f"{actor_instance.name} has {actor_instance.health} Health remaining"

        __class__.display_message(actor_health_message, 2)
        
    
    @staticmethod
    def actor_attack_message(attacker_instance:Combatant, damage_value:int) -> None:
        if not isinstance(attacker_instance, Combatant):
            raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))

        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, PlayableActor) == False:
            time.sleep(2)

        actor_attack_message = f"{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value} damage"
        
        __class__.display_message(actor_attack_message, 2)

    @staticmethod
    def actor_critical_attack_message(attacker_instance:Combatant, damage_value:int) -> None:
        if not isinstance(attacker_instance, Combatant):
            raise ValueError("The 'attacker_instance' parameter must be of type Combatant. Received type: {}".format(type(attacker_instance).__name__))

        if Interaction.global_game_mode == "MANUAL" and isinstance(attacker_instance, PlayableActor) == False:
            time.sleep(2)

        actor_critical_attack_message = f"""
{attacker_instance.name} attacks with {attacker_instance.attack_name} inflicting {damage_value * 2} damage
{attacker_instance.name} got a critical hit!!
"""
        __class__.display_message(actor_critical_attack_message, 2)



    # Battle Messages
    @staticmethod
    def battle_hud_message(player_party_instance:PlayerParty, enemy_party_instance:EnemyParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        if not isinstance(enemy_party_instance, EnemyParty):
            raise ValueError("The 'enemy_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(enemy_party_instance).__name__))

        battle_hud_message = ""

        for playable_instance in player_party_instance.members:
            battle_hud_message += f"{playable_instance.name}: {playable_instance.health}"
            battle_hud_message += "\n"
        battle_hud_message += "\n"

        for enemy_instance in enemy_party_instance.members:
            battle_hud_message += f"{enemy_instance.name}: {enemy_instance.health}\n"
            battle_hud_message += "\n"
  
        __class__.display_message(battle_hud_message, 2)
    
    @staticmethod
    def battle_start_message() -> None:
        battle_start_message = "The Battle Begins!"

        __class__.display_message(battle_start_message, 3)

    # Encounter Messages
    @staticmethod
    def distance_since_last(no_encounters_since:int) -> None:
        distance_since_last_message = f"After {no_encounters_since * 10} miles of travel"

        __class__.display_message(distance_since_last_message, 1)


    @staticmethod
    def flee_failure_message(player_name:str, enemy_name:str) -> None:
        flee_failure_message = f"{player_name} has Failed to Escape the {enemy_name}!"

        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)

        __class__.display_message(flee_failure_message, 1)
    
    @staticmethod
    def flee_success_message(player_name:str, enemy_name:str) -> None:
        flee_success_message = f"{player_name} has Successfully Escaped the {enemy_name}!"

        __class__.display_message(flee_success_message, 1)

    def special_encounter_message(progress_value:int, party_name:str,message_type:str)-> None:
        if message_type not in ["messages","success_messages","failure_messages"]:
            raise ValueError('Message type must be one of ["messages","success_messages","failure_messages"]')
        with open('encounters/story_events.json') as file:
            story_events_list = json.load(file)


        all_events = story_events_list['progress_events']

        current_event = all_events[str(progress_value)]
        for message in current_event[message_type]:
            formatted_message = message.format(party_name=party_name)
        
            __class__.display_message(formatted_message, 2)
            if Interaction.global_game_mode == "MANUAL":
                time.sleep(2)


    # Player Messages
    
    @staticmethod
    def post_game_recap(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))


        for player_instance in player_party_instance.members:
            player_report = f"""
Player Name: {player_instance.name}
Player Base Health: {player_instance.base_health}                             
Player Final Health: {player_instance.health}
Player Int: {player_instance.intellect}
Player Str: {player_instance.strength}
Player Agl: {player_instance.agility}
Player Lck: {player_instance.luck}
Player Gold: {player_instance.gold}
Player Potions: {player_instance.potions}
Player Attack Name: {player_instance.attack_name}
Player Attack Power: {player_instance.attack_power}
"""

            __class__.display_message(player_report, 2)



    @staticmethod
    def end_game_message(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        
        end_game_message = f"""
Fortranus the Ancient One has been Vanquished at the hands of {player_party_instance.name}


Your adventure has been completed, you may start a new adventure if you so choose
"""

        __class__.display_message(end_game_message, 2)

        if Interaction.global_game_mode == "MANUAL":
            save_game(player_party_instance)

    @staticmethod
    def empty_travel_message(empty_distance:int) -> None:
        if Interaction.global_game_mode == "MANUAL":
            time.sleep(2)
        empty_travel_message = f"{'.' * (empty_distance - 1 )}"

        __class__.display_message(empty_travel_message, 1)