from interaction.interaction_utilities import validate_input
from interaction.interaction_manual import manual_enemy_encounter, manual_in_battle, manual_post_battle
from interaction.interaction_automatic import auto_enemy_encounter, auto_in_battle, auto_post_battle

class Interaction:
    global_game_mode = "AUTO" ## this is a default value that should be can be updated to "MANUAL" during the welcome function
    global_player_count = "1" ## this is default value that can be updated to a new value in the welcome function
    
    @staticmethod
    def validate_input(choice_list:list, prompt_message:str):
        return validate_input(choice_list, prompt_message)

    @staticmethod
    def encounter_enemy():
        match __class__.global_game_mode:
            case "AUTO":
                player_action = auto_enemy_encounter()
                return player_action
            case "MANUAL":
                    player_action = manual_enemy_encounter()
                    return player_action
            case _:
                    print("Ummm How did you do that?, whatever just hit the thing")
                    return "ATTACK" 
    
    @staticmethod
    def post_battle(player_instance):
        match __class__.global_game_mode:
            case "AUTO":
                player_action = auto_post_battle(player_instance)
                return player_action
            case "MANUAL":
                  player_action = manual_post_battle()
                  return player_action
            case _:
                  print("Ummm How did you do that?, whatever.... Just.... Leave")
                  return "TRAVEL"


    @staticmethod
    def in_battle(player_instance):
        match __class__.global_game_mode:
            case "AUTO":
                player_action = auto_in_battle(player_instance)
                return player_action
            case "MANUAL":
                  player_action = manual_in_battle(player_instance.name)
                  return player_action
            case _:
                  print("Ummm How did you do that?, whatever just hit the thing")
                  return "ATTACK"
             

    @staticmethod
    def at_merchant(player_instance):
        while player_instance.potions < 100 and player_instance.gold != 0:
            if player_instance.gold != 0:
                player_instance.gold -= 25
                player_instance.potions += 1
                print(f"You purchase a potion. You now have {player_instance.potions}")
            else:
                 print("You do not have enough Gold to purchase more potions")
                 break