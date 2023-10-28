class Interaction:
    global_game_mode = "AUTO" ## this is a default value that should be can be updated to "MANUAL" during the welcome function
    global_player_count = "1" ## this is default value that can be updated to a new value in the welcome function

    @staticmethod
    def validate_input(choice_list:list, prompt_message:str):
         chosen_action = ""
         dumb_check = 0
         while chosen_action not in choice_list:
              chosen_action = input(prompt_message).upper()
              if chosen_action not in choice_list:
                   dumb_check += 1
                   print("Invalid Choice Try Again")
                   if dumb_check == 10:
                      print("Look it's not hard, just enter a valid choice....", end="\n\n")
                      exit()
              
         return chosen_action

    @staticmethod
    def post_battle(player_instance):
        match __class__.global_game_mode:
            case "AUTO":
                player_action =__class__._auto_post_battle(player_instance)
                return player_action
            case "MANUAL":
                  player_action = __class__._manual_post_battle()
                  return player_action
            case _:
                  print("Ummm How did you do that?, whatever.... Just.... Leave")
                  return "TRAVEL"


    @staticmethod
    def in_battle(player_instance):
        match __class__.global_game_mode:
            case "AUTO":
                player_action =__class__._auto_in_battle(player_instance)
                return player_action
            case "MANUAL":
                  player_action = __class__._manual_in_battle(player_instance.name)
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



## Hidden Methods

## Manual Interactions
    @staticmethod
    def _manual_in_battle(player_name):
        battle_options = ["ATTACK", "HEAL"]
        battle_message = f"""
{player_name}
Choose an Action:
ATTACK
HEAL

"""
        battle_choice = __class__.validate_input(battle_options, battle_message)
        return battle_choice
    
    @staticmethod
    def _manual_post_battle():
        post_battle_options = ["HEAL", "TRAVEL"]
        post_battle_message = """
Choose an Action:
HEAL
TRAVEL

"""     
        post_battle_choice = __class__.validate_input(post_battle_options, post_battle_message)
        return post_battle_choice


## Automatic Interactions
    @staticmethod
    def _auto_in_battle(player_instance):
        if player_instance.health <= 4 and player_instance.potions != 0:
            return "HEAL" 
        elif player_instance.potions == 0:
                print("You have no remaining potions and must make a stand!")
                return "ATTACK"
        else:
             return "ATTACK"
    @staticmethod
    def _auto_post_battle(player_instance):
        if player_instance.health < 20 and player_instance.potions != 0:
            return "HEAL"
        else:
             return "TRAVEL"