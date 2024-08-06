import random
from interaction.interaction_utilities import validate_input, sanitize, custom_text_entry
from logic.logic import select_combat_target
from message.message import Message
from interaction.interaction_manual import *

# Only Used For Type Hinting/Checking
from actors.actor_party import PlayerParty, EnemyParty
from actors.actor_playable import PlayableActor

class Interaction:
    global_game_mode = "AUTO" ## this is a default value that should be can be updated to "MANUAL" during the welcome function
    global_player_count = "1" ## this is default value that can be updated to a new value in the welcome function

    @staticmethod
    def choose_combat_target(enemy_party_instance:EnemyParty) -> int:
        if not isinstance(enemy_party_instance, EnemyParty):
            raise ValueError("The 'player_party_instance' parameter must be of type EnemyParty. Received type: {}".format(type(enemy_party_instance).__name__))
    
        match __class__.global_game_mode:
            case "AUTO":
                return select_combat_target(enemy_party_instance)
            case "MANUAL":
                return manual_choose_combat_target(enemy_party_instance)
            case _:
                return "ATTACK" 

    
    @staticmethod
    def encounter_enemy() -> str:
        match __class__.global_game_mode:
            case "AUTO":
                chosen_action = random.choice(["FLEE","ATTACK"])
                return chosen_action
            case "MANUAL":
                return manual_enemy_encounter()
            case _:
                return "ATTACK" 
    
    @staticmethod
    def post_battle(player_party_instance:PlayerParty) -> str:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        match __class__.global_game_mode:
            case "AUTO":
                for player_instance in player_party_instance.members:
                    if player_instance.health < 20 and player_instance.potions != 0:
                        chosen_action = "HEAL"
                chosen_action = "TRAVEL"

                return chosen_action
            case "MANUAL":
                return manual_post_battle()
            case _:
                return "TRAVEL"


    @staticmethod
    def in_battle(player_instance:PlayableActor) -> str:
        if not isinstance(player_instance, PlayableActor):
            raise ValueError("The 'player_instance' parameter must be of type PlayableActor. Received type: {}".format(type(player_instance).__name__))

        match __class__.global_game_mode:
            case "AUTO":
                if player_instance.health <= 40 and player_instance.potions != 0:
                    chosen_action = "HEAL" 
                elif player_instance.potions == 0:
                        Message.display_message(f"{player_instance.name} has no remaining potions and must make a stand!", 1)
                        chosen_action = "ATTACK"
                else:
                        chosen_action = random.choice(["EVADE","ATTACK","ATTACK","ATTACK"])
                
                return chosen_action
            case "MANUAL":
                return manual_in_battle(player_instance)
            case _:
                return "ATTACK"
             

    @staticmethod
    def at_merchant(player_party_instance:PlayerParty) -> None:
        if not isinstance(player_party_instance, PlayerParty):
            raise ValueError("The 'player_party_instance' parameter must be of type PlayerParty. Received type: {}".format(type(player_party_instance).__name__))

        Message.display_message("You arrive at a merchant", 1)
        match __class__.global_game_mode:
            case "AUTO":
                #init Counts
                player_count = 0
                gold_spent = 0
                potions_sold = 0

                for player_instance in player_party_instance.members:
                    player_count += 1
                    while player_instance.potions < 100 and player_instance.gold != 0:
                        if player_instance.spend_gold(25) == True:
                            gold_spent += 25

                            player_instance.gain_potion(1)
                            potions_sold += 1

                            Message.display_message(f"{player_instance.name} purchases a potion. They now have {player_instance.potions}", 1)
                        else:
                            Message.display_message(f"{player_instance.name} does not have enough Gold to purchase more potions", 1)
                            break
            case "MANUAL":
                manual_at_merchant(player_party_instance)
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def confirm_rest() -> bool:
        match __class__.global_game_mode:
            case "AUTO":
                return random.choice([True,True,False])
            case "MANUAL":
                return manual_confirm_rest()
            case _:
                raise ValueError("invalid game mode")

    @staticmethod
    def mystery_action() -> str:
        match __class__.global_game_mode:
            case "AUTO":
                return random.choice(["GREET","GREET","ATTACK"])
            case "MANUAL":
                return manual_mystery_action()
            case _:
                raise ValueError("invalid game mode")
    @staticmethod
    def loot_action() -> bool:
        match __class__.global_game_mode:
            case "AUTO":
                return random.choice(["OPEN","OPEN","LEAVE"])
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