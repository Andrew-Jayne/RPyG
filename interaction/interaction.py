from interaction.interaction_utilities import validate_input, sanitize, custom_text_entry
from interaction.interaction_manual import *
from interaction.interaction_automatic import *

class Interaction:
    global_game_mode = "AUTO" ## this is a default value that should be can be updated to "MANUAL" during the welcome function
    global_player_count = "1" ## this is default value that can be updated to a new value in the welcome function

    @staticmethod
    def choose_combat_target(enemy_party_instance):
        match __class__.global_game_mode:
            case "AUTO":
                return auto_choose_combat_target(enemy_party_instance)
            case "MANUAL":
                    return manual_choose_combat_target(enemy_party_instance)
            case _:
                    print("Ummm How did you do that?, whatever just hit the thing")
                    return "ATTACK" 

    
    @staticmethod
    def encounter_enemy():
        match __class__.global_game_mode:
            case "AUTO":
                return auto_enemy_encounter()
            case "MANUAL":
                    return manual_enemy_encounter()
            case _:
                    print("Ummm How did you do that?, whatever just hit the thing")
                    return "ATTACK" 
    
    @staticmethod
    def post_battle(player_party_instance):
        match __class__.global_game_mode:
            case "AUTO":
                return auto_post_battle(player_party_instance)
            case "MANUAL":
                  return manual_post_battle()
            case _:
                  print("Ummm How did you do that?, whatever.... Just.... Leave")
                  return "TRAVEL"


    @staticmethod
    def in_battle(player_instance):
        match __class__.global_game_mode:
            case "AUTO":
                return auto_in_battle(player_instance)
            case "MANUAL":
                  return manual_in_battle(player_instance.name)
            case _:
                  print("Ummm How did you do that?, whatever just hit the thing")
                  return "ATTACK"
             

    @staticmethod
    def at_merchant(player_party_instance):
        match __class__.global_game_mode:
            case "AUTO":
                auto_at_merchant(player_party_instance)
            case "MANUAL":
                manual_in_battle(player_party_instance)
            case _:
                print("Ummm How did you do that?, whatever.... Just.... Leave")


            
    @staticmethod
    def validate_input(choice_list:list, prompt_message:str):
        return validate_input(choice_list, prompt_message)
    
    @staticmethod
    def sanitize(input_string:str):
        return sanitize(input_string)
    
    @staticmethod
    def custom_text_entry(input_message:str, max_length:int):
         return custom_text_entry(input_message,max_length)