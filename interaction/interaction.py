from interaction.interaction_utilities import validate_input, sanitize, custom_text_entry
from interaction.interaction_manual import *
from interaction.interaction_automatic import *

# Only Used For Type Hinting/Checking
from actors.actor_party import PlayerParty, EnemyParty
from actors.actor_playable import PlayableActor

class Interaction:
    global_game_mode = "AUTO" ## this is a default value that should be can be updated to "MANUAL" during the welcome function
    global_player_count = "1" ## this is default value that can be updated to a new value in the welcome function

    @staticmethod
    def choose_combat_target(enemy_party_instance:EnemyParty):
        if not isinstance(enemy_party_instance, EnemyParty):
            raise ValueError("The 'player_party_instance' parameter must be of type EnemyParty. Received type: {}".format(type(enemy_party_instance).__name__))
    
        match __class__.global_game_mode:
            case "AUTO":
                return auto_choose_combat_target(enemy_party_instance)
            case "MANUAL":
                return manual_choose_combat_target(enemy_party_instance)
            case _:
                return "ATTACK" 

    
    @staticmethod
    def encounter_enemy():
        match __class__.global_game_mode:
            case "AUTO":
                return auto_enemy_encounter()
            case "MANUAL":
                return manual_enemy_encounter()
            case _:
                return "ATTACK" 
    
    @staticmethod
    def post_battle(player_party_instance:PlayerParty):
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        match __class__.global_game_mode:
            case "AUTO":
                return auto_post_battle(player_party_instance)
            case "MANUAL":
                return manual_post_battle()
            case _:
                return "TRAVEL"


    @staticmethod
    def in_battle(player_instance:PlayableActor):
        if not isinstance(player_instance, PlayableActor):
            raise ValueError("The 'player_instance' parameter must be of type PlayableActor. Received type: {}".format(type(player_instance).__name__))

        match __class__.global_game_mode:
            case "AUTO":
                return auto_in_battle(player_instance)
            case "MANUAL":
                return manual_in_battle(player_instance)
            case _:
                return "ATTACK"
             

    @staticmethod
    def at_merchant(player_party_instance:PlayerParty):
        from message.message import Message
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))
        

        Message.display_message("You arrive at a merchant", 1)
        match __class__.global_game_mode:
            case "AUTO":
                auto_at_merchant(player_party_instance)
            case "MANUAL":
                manual_at_merchant(player_party_instance)
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def confirm_rest() -> bool:
        match __class__.global_game_mode:
            case "AUTO":
                return auto_confirm_rest()
            case "MANUAL":
                return manual_confirm_rest()
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def mystery_action() -> str:
        match __class__.global_game_mode:
            case "AUTO":
                return auto_mystery_action()
            case "MANUAL":
                return manual_mystery_action()
            case _:
                raise ValueError("invalid game mode")
    @staticmethod
    def loot_action() -> bool:
        match __class__.global_game_mode:
            case "AUTO":
                return auto_loot_action()
            case "MANUAL":
                return manual_loot_action()
            case _:
                raise ValueError("invalid game mode")
    @staticmethod
    def embark() -> bool:
        match __class__.global_game_mode:
            case "AUTO":
                return True
            case "MANUAL":
                return manual_embark()
            case _:
                raise ValueError("invalid game mode")
    @staticmethod
    def accept_quest() -> bool:
            match __class__.global_game_mode:
                case "AUTO":
                    return True
                case "MANUAL":
                    return manual_accept_quest()
                case _:
                    raise ValueError("invalid game mode")


            
    @staticmethod
    def validate_input(choice_list:list[str], prompt_message:str):
        return validate_input(choice_list, prompt_message)
    
    @staticmethod
    def sanitize(input_string:str):
        return sanitize(input_string)
    
    @staticmethod
    def custom_text_entry(input_message:str, max_length:int):
         return custom_text_entry(input_message,max_length)